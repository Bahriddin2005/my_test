#!/usr/bin/env python
"""
Matematika fanidan 50 ta test yaratish scripti
Har bir testda turli mavzularda savollar bo'ladi
"""
import os
import sys
import django
import random

# Django setup
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mytest.settings')
django.setup()

from tests_app.models import Test, Question, Choice
from accounts.models import User
from django.db import transaction

def generate_math_questions():
    """Matematika fanidan turli mavzularda savollar yaratish"""
    
    questions_templates = [
        # Arifmetika savollari
        {
            'topic': 'Qo\'shish',
            'questions': [
                {'text': '{} + {} = ?', 'type': 'single_choice', 'points': 1},
                {'text': '{} + {} + {} = ?', 'type': 'single_choice', 'points': 2},
                {'text': '{} va {} yig\'indisi necha?', 'type': 'single_choice', 'points': 1},
            ]
        },
        {
            'topic': 'Ayirish',
            'questions': [
                {'text': '{} - {} = ?', 'type': 'single_choice', 'points': 1},
                {'text': '{} dan {} ni ayirsak necha bo\'ladi?', 'type': 'single_choice', 'points': 1},
                {'text': '{} - {} - {} = ?', 'type': 'single_choice', 'points': 2},
            ]
        },
        {
            'topic': 'Ko\'paytirish',
            'questions': [
                {'text': '{} × {} = ?', 'type': 'single_choice', 'points': 1},
                {'text': '{} ni {} ga ko\'paytirsak necha bo\'ladi?', 'type': 'single_choice', 'points': 1},
                {'text': '{} × {} × {} = ?', 'type': 'single_choice', 'points': 2},
            ]
        },
        {
            'topic': 'Bo\'lish',
            'questions': [
                {'text': '{} ÷ {} = ?', 'type': 'single_choice', 'points': 1},
                {'text': '{} ni {} ga bo\'lsak necha bo\'ladi?', 'type': 'single_choice', 'points': 1},
                {'text': '{} ÷ {} ÷ {} = ?', 'type': 'single_choice', 'points': 2},
            ]
        },
        {
            'topic': 'Sonlarni solishtirish',
            'questions': [
                {'text': 'Qaysi son katta: {} yoki {}?', 'type': 'single_choice', 'points': 1},
                {'text': 'Qaysi sonlar {} dan kichik?', 'type': 'multiple_choice', 'points': 2},
                {'text': 'Qaysi sonlar {} dan katta?', 'type': 'multiple_choice', 'points': 2},
            ]
        },
        {
            'topic': 'Juft va toq sonlar',
            'questions': [
                {'text': '{} soni juft yoki toq?', 'type': 'single_choice', 'points': 1},
                {'text': 'Qaysi sonlar juft?', 'type': 'multiple_choice', 'points': 2},
                {'text': 'Qaysi sonlar toq?', 'type': 'multiple_choice', 'points': 2},
            ]
        },
        {
            'topic': 'Kasrlar',
            'questions': [
                {'text': '{}/{} + {}/{} = ?', 'type': 'single_choice', 'points': 2},
                {'text': '{}/{} - {}/{} = ?', 'type': 'single_choice', 'points': 2},
                {'text': '{}/{} × {}/{} = ?', 'type': 'single_choice', 'points': 2},
            ]
        },
        {
            'topic': 'Foizlar',
            'questions': [
                {'text': '{} ning {}% i necha?', 'type': 'single_choice', 'points': 2},
                {'text': '{} son {} ning necha foizi?', 'type': 'single_choice', 'points': 2},
                {'text': '{} foiz {} dan necha?', 'type': 'single_choice', 'points': 2},
            ]
        },
        {
            'topic': 'Geometriya',
            'questions': [
                {'text': 'Kvadratning perimetri {} sm bo\'lsa, tomoni necha sm?', 'type': 'single_choice', 'points': 2},
                {'text': 'To\'rtburchakning uzunligi {} sm, eni {} sm. Perimetri necha?', 'type': 'single_choice', 'points': 2},
                {'text': 'Doiraning radiusi {} sm bo\'lsa, diametri necha sm?', 'type': 'single_choice', 'points': 1},
            ]
        },
        {
            'topic': 'O\'lchovlar',
            'questions': [
                {'text': '{} metr necha santimetr?', 'type': 'single_choice', 'points': 1},
                {'text': '{} kilogramm necha gramm?', 'type': 'single_choice', 'points': 1},
                {'text': '{} litr necha millilitr?', 'type': 'single_choice', 'points': 1},
            ]
        },
    ]
    
    return questions_templates

def generate_question_data(template, grade):
    """Savol ma'lumotlarini yaratish"""
    question_text = template['text']
    question_type = template['type']
    
    # Sonlarni yaratish
    if grade <= 4:
        nums = [random.randint(1, 100) for _ in range(question_text.count('{}'))]
    elif grade <= 7:
        nums = [random.randint(1, 1000) for _ in range(question_text.count('{}'))]
    else:
        nums = [random.randint(1, 10000) for _ in range(question_text.count('{}'))]
    
    # Savol matnini to'ldirish
    formatted_text = question_text.format(*nums)
    
    # Javobni hisoblash
    if 'Qo\'shish' in template.get('topic', ''):
        if len(nums) == 2:
            correct_answer = nums[0] + nums[1]
        else:
            correct_answer = sum(nums)
    elif 'Ayirish' in template.get('topic', ''):
        if len(nums) == 2:
            correct_answer = nums[0] - nums[1]
        else:
            correct_answer = nums[0] - nums[1] - nums[2]
    elif 'Ko\'paytirish' in template.get('topic', ''):
        if len(nums) == 2:
            correct_answer = nums[0] * nums[1]
        else:
            correct_answer = nums[0] * nums[1] * nums[2]
    elif 'Bo\'lish' in template.get('topic', ''):
        if len(nums) == 2:
            correct_answer = nums[0] // nums[1] if nums[1] != 0 else nums[0]
        else:
            correct_answer = (nums[0] // nums[1]) // nums[2] if nums[1] != 0 and nums[2] != 0 else nums[0]
    elif 'Solishtirish' in template.get('topic', ''):
        correct_answer = max(nums) if len(nums) == 2 else nums[0]
    elif 'Juft' in template.get('topic', ''):
        correct_answer = 'juft' if nums[0] % 2 == 0 else 'toq'
    elif 'Foiz' in template.get('topic', ''):
        if 'ning' in question_text and '%' in question_text:
            correct_answer = int(nums[0] * nums[1] / 100)
        else:
            correct_answer = int((nums[0] / nums[1]) * 100) if nums[1] != 0 else 0
    elif 'Geometriya' in template.get('topic', ''):
        if 'perimetri' in question_text and 'tomoni' in question_text:
            correct_answer = nums[0] // 4
        elif 'Perimetri' in question_text:
            correct_answer = (nums[0] + nums[1]) * 2
        elif 'diametri' in question_text:
            correct_answer = nums[0] * 2
        else:
            correct_answer = nums[0]
    elif 'O\'lchovlar' in template.get('topic', ''):
        if 'metr' in question_text and 'santimetr' in question_text:
            correct_answer = nums[0] * 100
        elif 'kilogramm' in question_text and 'gramm' in question_text:
            correct_answer = nums[0] * 1000
        elif 'litr' in question_text and 'millilitr' in question_text:
            correct_answer = nums[0] * 1000
        else:
            correct_answer = nums[0]
    else:
        correct_answer = nums[0] if nums else 0
    
    # Variantlar yaratish
    choices = []
    if question_type == 'single_choice':
        # To'g'ri javob
        choices.append({'text': str(correct_answer), 'is_correct': True})
        # Noto'g'ri javoblar
        wrong_answers = [
            correct_answer + random.randint(1, 10),
            correct_answer - random.randint(1, 10),
            correct_answer + random.randint(11, 20),
        ]
        for wrong in wrong_answers:
            if wrong != correct_answer and wrong > 0:
                choices.append({'text': str(wrong), 'is_correct': False})
    else:  # multiple_choice
        # Bir nechta to'g'ri javoblar
        if 'kichik' in formatted_text.lower():
            threshold = nums[0] if nums else 50
            correct_answers = [n for n in nums[1:] if n < threshold] if len(nums) > 1 else [nums[0] - 1, nums[0] - 2]
            wrong_answers = [n for n in nums[1:] if n >= threshold] if len(nums) > 1 else [nums[0] + 1, nums[0] + 2]
        elif 'katta' in formatted_text.lower():
            threshold = nums[0] if nums else 50
            correct_answers = [n for n in nums[1:] if n > threshold] if len(nums) > 1 else [nums[0] + 1, nums[0] + 2]
            wrong_answers = [n for n in nums[1:] if n <= threshold] if len(nums) > 1 else [nums[0] - 1, nums[0] - 2]
        elif 'juft' in formatted_text.lower():
            correct_answers = [n for n in nums if n % 2 == 0]
            wrong_answers = [n for n in nums if n % 2 != 0]
        else:
            correct_answers = nums[:2] if len(nums) >= 2 else [nums[0]]
            wrong_answers = [n + random.randint(5, 15) for n in nums[2:]] if len(nums) > 2 else [nums[0] + 1, nums[0] + 2]
        
        for ans in correct_answers:
            choices.append({'text': str(ans), 'is_correct': True})
        for ans in wrong_answers[:4-len(correct_answers)]:
            choices.append({'text': str(ans), 'is_correct': False})
    
    # Kamida 4 ta variant bo'lishi kerak
    while len(choices) < 4:
        new_wrong = correct_answer + random.randint(20, 50) if isinstance(correct_answer, int) else random.randint(1, 100)
        choices.append({'text': str(new_wrong), 'is_correct': False})
    
    # Variantlarni aralashtirish
    random.shuffle(choices)
    
    return {
        'question_text': formatted_text,
        'question_type': question_type,
        'points': template['points'],
        'choices': choices[:4],  # Faqat 4 ta variant
        'explanation': f"To'g'ri javob: {correct_answer}"
    }

def create_50_math_tests():
    """Matematika fanidan 50 ta test yaratish"""
    
    # Admin yoki teacher foydalanuvchisini topish
    admin = User.objects.filter(role='admin').first()
    if not admin:
        teacher = User.objects.filter(role='teacher').first()
        if not teacher:
            print("❌ Admin yoki teacher foydalanuvchi topilmadi!")
            print("Iltimos, avval admin yoki teacher foydalanuvchi yarating.")
            return
        creator = teacher
    else:
        creator = admin
    
    print(f"✓ Testlar yaratuvchi: {creator.username} ({creator.role})")
    print("\n" + "="*60)
    print("Matematika fanidan 50 ta test yaratilmoqda...")
    print("="*60 + "\n")
    
    questions_templates = generate_math_questions()
    
    # Sinflar ro'yxati (1-11)
    grades = list(range(1, 12))
    
    # Mavzular ro'yxati
    topics = [
        'Sonlar va Hisoblar', 'Geometrik Shakllar', 'O\'lchovlar va Vaqt',
        'Kasrlar', 'Foizlar', 'Tengsizliklar', 'Funksiyalar', 'Tenglamalar',
        'Proportsiyalar', 'Statistika', 'Ehtimollik', 'Algebra', 'Geometriya',
        'Trigonometriya', 'Logarifmlar', 'Derivatalar', 'Integrallar'
    ]
    
    created_count = 0
    
    with transaction.atomic():
        for test_num in range(1, 51):
            # Random sinf tanlash
            grade = random.choice(grades)
            
            # Random mavzu tanlash
            topic = random.choice(topics)
            
            # Test nomi
            title = f'Matematika - {topic} (Test {test_num})'
            
            # Test mavjudligini tekshirish
            existing_test = Test.objects.filter(title=title).first()
            if existing_test:
                print(f"⚠️  Test allaqachon mavjud: {title}")
                continue
            
            # Test yaratish
            test = Test.objects.create(
                title=title,
                description=f'{grade}-sinf uchun {topic} mavzusida test',
                subject='Matematika',
                grade=grade,
                created_by=creator,
                time_limit=random.randint(20, 60),
                is_active=True,
                max_attempts=1,
                show_results=True,
                shuffle_questions=True
            )
            
            print(f"✓ Test {test_num}/50 yaratildi: {title} ({grade}-sinf)")
            
            # Har bir test uchun 10-20 ta savol yaratish
            num_questions = random.randint(10, 20)
            questions_created = 0
            
            for q_num in range(1, num_questions + 1):
                # Random savol shablonini tanlash
                topic_template = random.choice(questions_templates)
                question_template = random.choice(topic_template['questions'])
                
                try:
                    question_data = generate_question_data(question_template, grade)
                    
                    question = Question.objects.create(
                        test=test,
                        question_text=question_data['question_text'],
                        question_type=question_data['question_type'],
                        points=question_data['points'],
                        order=q_num,
                        explanation=question_data.get('explanation', '')
                    )
                    
                    # Variantlar yaratish
                    if question_data.get('choices'):
                        for choice_data in question_data['choices']:
                            Choice.objects.create(
                                question=question,
                                choice_text=choice_data['text'],
                                is_correct=choice_data['is_correct']
                            )
                    
                    questions_created += 1
                except Exception as e:
                    print(f"  ⚠️  Savol yaratishda xatolik: {e}")
                    continue
            
            print(f"  ✓ {questions_created} ta savol qo'shildi")
            created_count += 1
            
            if test_num % 10 == 0:
                print(f"\n📊 Progress: {test_num}/50 testlar yaratildi\n")
    
    print("\n" + "="*60)
    print(f"✅ Jami {created_count} ta test yaratildi!")
    print("="*60)

if __name__ == '__main__':
    create_50_math_tests()

