from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import User, VerificationRequest
import json

def signup_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['username', 'email', 'password', 'role']
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse({'error': f'{field} is required'}, status=400)
            
            # Check if user exists
            if User.objects.filter(username=data['username']).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)
            
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'error': 'Email already exists'}, status=400)
            
            # Validate email domain
            email_domain = data['email'].split('@')[-1]
            allowed_domains = ['buxorobilimdonlar.uz', 'student.buxorobilimdonlar.uz']
            if email_domain not in allowed_domains:
                return JsonResponse({'error': 'Email must be from school domain'}, status=400)
            
            # Create user
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                first_name=data.get('first_name', ''),
                last_name=data.get('last_name', ''),
                role=data['role']
            )
            
            # Set additional fields based on role
            if data['role'] == 'student':
                user.student_id = data.get('student_id')
                user.class_name = data.get('class_name')
                user.grade = data.get('grade')
            elif data['role'] == 'teacher':
                user.subject = data.get('subject')
            
            user.phone_number = data.get('phone_number')
            user.save()
            
            # Create verification request
            VerificationRequest.objects.create(user=user)
            
            return JsonResponse({
                'message': 'Account created successfully. Please wait for admin approval.',
                'user_id': user.id
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An error occurred during registration'}, status=500)
    
    return render(request, 'accounts/signup.html')

def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username_or_email = data.get('username')
            password = data.get('password')
            
            if not username_or_email or not password:
                return JsonResponse({'error': 'Username/Email and password are required'}, status=400)
            
            # Try to authenticate with username first
            user = authenticate(request, username=username_or_email, password=password)
            
            # If that fails, try to find user by email and authenticate
            if user is None:
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if user is not None:
                if not user.is_verified:
                    return JsonResponse({'error': 'Account not verified yet. Please wait for admin approval.'}, status=403)
                
                login(request, user)
                return JsonResponse({
                    'message': 'Login successful',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'role': user.role,
                        'email': user.email,
                        'is_verified': user.is_verified
                    }
                })
            else:
                return JsonResponse({'error': 'Invalid username/email or password'}, status=401)
                
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An error occurred during login'}, status=500)
    
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logged out successfully'})

@login_required
def dashboard_view(request):
    from tests_app.models import TestResult, TestAttempt, Test
    
    context = {
        'user': request.user,
        'verification_requests_count': 0
    }
    
    if request.user.role == 'admin':
        # Admin uchun statistikalarni hisoblash
        context['verification_requests_count'] = VerificationRequest.objects.filter(is_approved=None).count()
        context['total_students'] = User.objects.filter(role='student').count()
        context['total_teachers'] = User.objects.filter(role='teacher').count()
        context['total_tests'] = Test.objects.count()
    elif request.user.role == 'student':
        # O'quvchi uchun natijalarni olish
        test_results = TestResult.objects.filter(
            attempt__student=request.user
        ).select_related('attempt', 'attempt__test').order_by('-attempt__started_at')[:5]
        
        context['recent_results'] = []
        for result in test_results:
            # Grade ni hisoblash - безопасная версия
            try:
                if (result.attempt and 
                    result.attempt.score is not None and 
                    result.attempt.total_points is not None and 
                    result.attempt.total_points > 0):
                    percentage = (result.attempt.score / result.attempt.total_points * 100)
                else:
                    percentage = 0
            except (TypeError, ZeroDivisionError):
                percentage = 0
                
            if percentage >= 81:
                grade = "A'lo"
            elif percentage >= 61:
                grade = 'Yaxshi'
            elif percentage >= 31:
                grade = 'Qoniqarli'
            else:
                grade = 'Qoniqarsiz'
                
            context['recent_results'].append({
                'test_name': result.attempt.test.title,
                'score': result.attempt.score,
                'max_score': result.attempt.total_points,
                'percentage': percentage,
                'grade': grade,
                'created_at': result.attempt.started_at,
                'test_id': result.attempt.test.id
            })
        
        # Umumiy statistika
        all_results = TestResult.objects.filter(attempt__student=request.user)
        context['total_tests'] = all_results.count()
        
        if all_results:
            # Безопасное вычисление среднего балла
            total_percentage = 0
            valid_results = 0
            
            for r in all_results:
                try:
                    if (r.attempt and 
                        r.attempt.score is not None and 
                        r.attempt.total_points is not None and 
                        r.attempt.total_points > 0):
                        total_percentage += (r.attempt.score / r.attempt.total_points * 100)
                        valid_results += 1
                except (TypeError, ZeroDivisionError):
                    continue
            
            context['average_score'] = total_percentage / valid_results if valid_results > 0 else 0
            
            # Безопасное нахождение лучшего результата
            best_result = None
            best_percentage = 0
            
            for r in all_results:
                try:
                    if (r.attempt and 
                        r.attempt.score is not None and 
                        r.attempt.total_points is not None and 
                        r.attempt.total_points > 0):
                        current_percentage = (r.attempt.score / r.attempt.total_points * 100)
                        if current_percentage > best_percentage:
                            best_percentage = current_percentage
                            best_result = r
                except (TypeError, ZeroDivisionError):
                    continue
            
            if best_result:
                # Grade ni hisoblash
                if best_percentage >= 81:
                    best_grade = "A'lo"
                elif best_percentage >= 61:
                    best_grade = 'Yaxshi'
                elif best_percentage >= 31:
                    best_grade = 'Qoniqarli'
                else:
                    best_grade = 'Qoniqarsiz'
                    
                context['best_result'] = {
                    'test_name': best_result.attempt.test.title,
                    'score': best_result.attempt.score,
                    'max_score': best_result.attempt.total_points,
                    'percentage': best_percentage,
                    'grade': best_grade
                }
            else:
                context['best_result'] = {
                    'test_name': 'No tests completed',
                    'score': 0,
                    'max_score': 0,
                    'percentage': 0,
                    'grade': 'No grade'
                }
        else:
            context['average_score'] = 0
            context['best_result'] = {
                'test_name': 'No tests completed',
                'score': 0,
                'max_score': 0,
                'percentage': 0,
                'grade': 'No grade'
            }
    
    return render(request, 'accounts/dashboard.html', context)

@login_required
def profile_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.user
            
            # Update allowed fields
            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)
            user.phone_number = data.get('phone_number', user.phone_number)
            
            if user.role == 'student':
                user.class_name = data.get('class_name', user.class_name)
            elif user.role == 'teacher':
                user.subject = data.get('subject', user.subject)
            
            user.save()
            
            return JsonResponse({'message': 'Profile updated successfully'})
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An error occurred'}, status=500)
    
    return render(request, 'accounts/profile.html')

@login_required
def verification_requests_view(request):
    if request.user.role != 'admin':
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    if request.method == 'GET' and request.headers.get('Accept') == 'application/json':
        # Sinf bo'yicha tartiblab olish
        requests = VerificationRequest.objects.filter(is_approved=None).select_related('user').order_by('user__grade', 'user__class_name', 'user__first_name')
        requests_data = [{
            'id': req.id,
            'user': {
                'id': req.user.id,
                'username': req.user.username,
                'email': req.user.email,
                'first_name': req.user.first_name,
                'last_name': req.user.last_name,
                'role': req.user.role,
                'student_id': req.user.student_id,
                'class_name': req.user.class_name,
                'grade': req.user.grade,
                'subject': req.user.subject,
            },
            'requested_at': req.requested_at.isoformat()
        } for req in requests]
        
        return JsonResponse({'requests': requests_data})
    
    return render(request, 'accounts/verification_requests.html')

@login_required
@require_http_methods(["POST"])
def approve_verification(request, request_id):
    if request.user.role != 'admin':
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        verification_request = VerificationRequest.objects.get(id=request_id)
        verification_request.is_approved = True
        verification_request.processed_by = request.user
        verification_request.processed_at = timezone.now()
        verification_request.save()
        
        # Verify the user
        verification_request.user.is_verified = True
        verification_request.user.save()
        
        return JsonResponse({'message': 'User verified successfully'})
    
    except VerificationRequest.DoesNotExist:
        return JsonResponse({'error': 'Verification request not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred'}, status=500)

@login_required
@require_http_methods(["POST"])
def reject_verification(request, request_id):
    if request.user.role != 'admin':
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        data = json.loads(request.body)
        verification_request = VerificationRequest.objects.get(id=request_id)
        verification_request.is_approved = False
        verification_request.processed_by = request.user
        verification_request.processed_at = timezone.now()
        verification_request.rejection_reason = data.get('reason', '')
        verification_request.save()
        
        return JsonResponse({'message': 'Verification request rejected'})
    
    except VerificationRequest.DoesNotExist:
        return JsonResponse({'error': 'Verification request not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred'}, status=500)

@login_required
def analytics_view(request):
    """Web sayt analitikasi - Faqat admin uchun"""
    if request.user.role != 'admin':
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        from tests_app.models import Test, TestAttempt, TestResult, Question
        from django.db.models import Count, Avg, Q, Sum
        from django.utils import timezone
        from datetime import timedelta
        
        # Umumiy statistika
        total_students = User.objects.filter(role='student', is_verified=True).count()
        total_teachers = User.objects.filter(role='teacher', is_verified=True).count()
        total_tests = Test.objects.count()
        total_questions = Question.objects.count()
        total_attempts = TestAttempt.objects.filter(is_completed=True).count()
    
    # Test natijalari statistikasi
    completed_attempts = TestAttempt.objects.filter(is_completed=True)
    if completed_attempts.exists():
        avg_score = completed_attempts.aggregate(avg=Avg('percentage'))['avg'] or 0
        total_score = completed_attempts.aggregate(total=Sum('score'))['total'] or 0
        total_points = completed_attempts.aggregate(total=Sum('total_points'))['total'] or 0
    else:
        avg_score = 0
        total_score = 0
        total_points = 0
        
        # Sinf bo'yicha statistika
        grade_stats = []
    for grade in range(5, 12):
        students_count = User.objects.filter(role='student', grade=grade, is_verified=True).count()
        tests_count = Test.objects.filter(grade=grade).count()
        attempts_count = TestAttempt.objects.filter(
            is_completed=True,
            student__grade=grade
        ).count()
        
        if attempts_count > 0:
            grade_avg = TestAttempt.objects.filter(
                is_completed=True,
                student__grade=grade
            ).aggregate(avg=Avg('percentage'))['avg'] or 0
        else:
            grade_avg = 0
        
        grade_stats.append({
            'grade': grade,
            'students': students_count,
            'tests': tests_count,
            'attempts': attempts_count,
            'avg_score': round(grade_avg, 1)
        })
        
        # Fan bo'yicha statistika
        subject_stats = []
    subjects = Test.objects.values_list('subject', flat=True).distinct()
    for subject in subjects:
        tests_count = Test.objects.filter(subject=subject).count()
        attempts_count = TestAttempt.objects.filter(
            is_completed=True,
            test__subject=subject
        ).count()
        
        if attempts_count > 0:
            subject_avg = TestAttempt.objects.filter(
                is_completed=True,
                test__subject=subject
            ).aggregate(avg=Avg('percentage'))['avg'] or 0
        else:
            subject_avg = 0
        
        subject_stats.append({
            'subject': subject,
            'tests': tests_count,
            'attempts': attempts_count,
            'avg_score': round(subject_avg, 1)
        })
        
        # Eng faol o'quvchilar (top 10)
        top_students = User.objects.filter(
        role='student',
        is_verified=True
    ).annotate(
        attempts_count=Count('test_attempts', filter=Q(test_attempts__is_completed=True))
    ).order_by('-attempts_count')[:10]
    
    top_students_data = []
    for student in top_students:
        if student.attempts_count > 0:
            student_avg = TestAttempt.objects.filter(
                student=student,
                is_completed=True
            ).aggregate(avg=Avg('percentage'))['avg'] or 0
        else:
            student_avg = 0
        
        top_students_data.append({
            'name': student.get_full_name() or student.username,
            'grade': student.grade,
            'class_name': student.class_name,
            'attempts': student.attempts_count,
            'avg_score': round(student_avg, 1)
        })
        
        # Eng muvaffaqiyatli testlar (top 10)
        top_tests = Test.objects.annotate(
        attempts_count=Count('attempts', filter=Q(attempts__is_completed=True))
    ).filter(attempts_count__gt=0).order_by('-attempts_count')[:10]
    
    top_tests_data = []
    for test in top_tests:
        test_attempts = TestAttempt.objects.filter(test=test, is_completed=True)
        if test_attempts.exists():
            test_avg = test_attempts.aggregate(avg=Avg('percentage'))['avg'] or 0
        else:
            test_avg = 0
        
        top_tests_data.append({
            'title': test.title,
            'subject': test.subject,
            'grade': test.grade,
            'attempts': test.attempts_count,
            'avg_score': round(test_avg, 1),
            'total_questions': test.total_questions
        })
        
        # Vaqt bo'yicha statistika (oxirgi 30 kun)
        date_stats = []
    for i in range(30):
        date = timezone.now().date() - timedelta(days=i)
        attempts_count = TestAttempt.objects.filter(
            is_completed=True,
            finished_at__date=date
        ).count()
        date_stats.append({
            'date': date.isoformat(),
            'attempts': attempts_count
        })
        date_stats.reverse()
        
        # Baho bo'yicha taqsimot
        grade_distribution_alo = TestResult.objects.filter(grade="A'lo").count()
        grade_distribution_yaxshi = TestResult.objects.filter(grade='Yaxshi').count()
        grade_distribution_qoniqarli = TestResult.objects.filter(grade='Qoniqarli').count()
        grade_distribution_qoniqarsiz = TestResult.objects.filter(grade='Qoniqarsiz').count()
        
        # O'quvchilar ro'yxati - login vaqtlari bilan
        students_list = User.objects.filter(
            role='student',
            is_verified=True
        ).order_by('-last_login', '-date_joined')[:50]  # Oxirgi 50 ta
        
        students_data = []
        for student in students_list:
            try:
                students_data.append({
                    'id': student.id,
                    'name': student.get_full_name() or student.username,
                    'username': student.username,
                    'grade': student.grade or '-',
                    'class_name': student.class_name or '-',
                    'last_login': student.last_login.strftime('%Y-%m-%d %H:%M:%S') if student.last_login else 'Hech qachon',
                    'date_joined': student.date_joined.strftime('%Y-%m-%d %H:%M:%S') if student.date_joined else '',
                    'is_online': student.last_login and (timezone.now() - student.last_login).total_seconds() < 3600 if student.last_login else False
                })
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f'Error processing student {student.id}: {str(e)}')
                continue
        
        # O'qituvchilar ro'yxati - login vaqtlari bilan
        teachers_list = User.objects.filter(
            role='teacher',
            is_verified=True
        ).order_by('-last_login', '-date_joined')[:50]  # Oxirgi 50 ta
        
        teachers_data = []
        for teacher in teachers_list:
            try:
                teachers_data.append({
                    'id': teacher.id,
                    'name': teacher.get_full_name() or teacher.username,
                    'username': teacher.username,
                    'subject': teacher.subject or '-',
                    'last_login': teacher.last_login.strftime('%Y-%m-%d %H:%M:%S') if teacher.last_login else 'Hech qachon',
                    'date_joined': teacher.date_joined.strftime('%Y-%m-%d %H:%M:%S') if teacher.date_joined else '',
                    'is_online': teacher.last_login and (timezone.now() - teacher.last_login).total_seconds() < 3600 if teacher.last_login else False
                })
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f'Error processing teacher {teacher.id}: {str(e)}')
                continue
        
        context = {
            'total_students': total_students,
            'total_teachers': total_teachers,
            'total_tests': total_tests,
            'total_questions': total_questions,
            'total_attempts': total_attempts,
            'avg_score': round(avg_score, 1) if avg_score else 0,
            'total_score': total_score or 0,
            'total_points': total_points or 0,
            'grade_stats': grade_stats,
            'subject_stats': subject_stats,
            'top_students': top_students_data,
            'top_tests': top_tests_data,
            'date_stats': date_stats,
            'grade_distribution_alo': grade_distribution_alo,
            'grade_distribution_yaxshi': grade_distribution_yaxshi,
            'grade_distribution_qoniqarli': grade_distribution_qoniqarli,
            'grade_distribution_qoniqarsiz': grade_distribution_qoniqarsiz,
            'students_list': students_data,
            'teachers_list': teachers_data
        }
        
        if request.headers.get('Accept') == 'application/json':
            return JsonResponse(context)
        
        return render(request, 'accounts/analytics.html', context)
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f'Error in analytics_view: {str(e)}', exc_info=True)
        
        # Xatolik holatida minimal context bilan sahifani ko'rsatish
        error_context = {
            'total_students': 0,
            'total_teachers': 0,
            'total_tests': 0,
            'total_questions': 0,
            'total_attempts': 0,
            'avg_score': 0,
            'total_score': 0,
            'total_points': 0,
            'grade_stats': [],
            'subject_stats': [],
            'top_students': [],
            'top_tests': [],
            'date_stats': [],
            'grade_distribution_alo': 0,
            'grade_distribution_yaxshi': 0,
            'grade_distribution_qoniqarli': 0,
            'grade_distribution_qoniqarsiz': 0,
            'students_list': [],
            'teachers_list': [],
            'error_message': 'Ma\'lumotlarni yuklashda xatolik yuz berdi. Iltimos, qayta urinib ko\'ring.'
        }
        
        if request.headers.get('Accept') == 'application/json':
            return JsonResponse({
                'error': 'Ma\'lumotlarni yuklashda xatolik yuz berdi',
                'detail': str(e)
            }, status=500)
        
        return render(request, 'accounts/analytics.html', error_context)
