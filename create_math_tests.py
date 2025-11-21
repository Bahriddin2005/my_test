#!/usr/bin/env python
"""
Matematika fanidan 4-sinf uchun testlar yaratish scripti
"""
import os
import sys
import django

# Django setup
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mytest.settings')
django.setup()

from tests_app.models import Test, Question, Choice
from accounts.models import User
from django.utils import timezone

def create_math_tests():
    """Matematika fanidan 4-sinf uchun testlar yaratish"""
    
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
    print("Matematika fanidan 4-sinf uchun testlar yaratilmoqda...")
    print("="*60 + "\n")
    
    # Test 1: Sonlar va hisoblar
    test1_data = {
        'title': 'Matematika - Sonlar va Hisoblar',
        'description': '4-sinf uchun sonlar va asosiy hisoblar mavzusida test',
        'subject': 'Matematika',
        'grade': 4,
        'time_limit': 30,
        'questions': [
            {
                'question_text': '25 + 17 = ?',
                'question_type': 'single_choice',
                'points': 2,
                'explanation': '25 + 17 = 42',
                'choices': [
                    {'text': '40', 'is_correct': False},
                    {'text': '42', 'is_correct': True},
                    {'text': '44', 'is_correct': False},
                    {'text': '45', 'is_correct': False},
                ]
            },
            {
                'question_text': '50 - 23 = ?',
                'question_type': 'single_choice',
                'points': 2,
                'explanation': '50 - 23 = 27',
                'choices': [
                    {'text': '25', 'is_correct': False},
                    {'text': '27', 'is_correct': True},
                    {'text': '29', 'is_correct': False},
                    {'text': '30', 'is_correct': False},
                ]
            },
            {
                'question_text': '6 × 7 = ?',
                'question_type': 'single_choice',
                'points': 2,
                'explanation': '6 × 7 = 42',
                'choices': [
                    {'text': '40', 'is_correct': False},
                    {'text': '42', 'is_correct': True},
                    {'text': '44', 'is_correct': False},
                    {'text': '48', 'is_correct': False},
                ]
            },
            {
                'question_text': '48 ÷ 6 = ?',
                'question_type': 'single_choice',
                'points': 2,
                'explanation': '48 ÷ 6 = 8',
                'choices': [
                    {'text': '6', 'is_correct': False},
                    {'text': '7', 'is_correct': False},
                    {'text': '8', 'is_correct': True},
                    {'text': '9', 'is_correct': False},
                ]
            },
            {
                'question_text': 'Qaysi sonlar 100 dan kichik?',
                'question_type': 'multiple_choice',
                'points': 3,
                'explanation': '95, 88 va 67 sonlar 100 dan kichik',
                'choices': [
                    {'text': '95', 'is_correct': True},
                    {'text': '88', 'is_correct': True},
                    {'text': '105', 'is_correct': False},
                    {'text': '67', 'is_correct': True},
                ]
            },
        ]
    }
    
    # Test 2: Geometrik shakllar
    test2_data = {
        'title': 'Matematika - Geometrik Shakllar',
        'description': '4-sinf uchun geometrik shakllar mavzusida test',
        'subject': 'Matematika',
        'grade': 4,
        'time_limit': 25,
        'questions': [
            {
                'question_text': 'Qaysi shakl 4 ta teng tomonli va 4 ta to\'g\'ri burchakli?',
                'question_type': 'single_choice',
                'points': 2,
                'explanation': 'Kvadrat 4 ta teng tomonli va 4 ta to\'g\'ri burchakli',
                'choices': [
                    {'text': 'Uchburchak', 'is_correct': False},
                    {'text': 'Kvadrat', 'is_correct': True},
                    {'text': 'Doira', 'is_correct': False},
                    {'text': 'Oval', 'is_correct': False},
                ]
            },
            {
                'question_text': 'Uchburchakning nechta tomoni bor?',
                'question_type': 'single_choice',
                'points': 1,
                'explanation': 'Uchburchakning 3 ta tomoni bor',
                'choices': [
                    {'text': '2', 'is_correct': False},
                    {'text': '3', 'is_correct': True},
                    {'text': '4', 'is_correct': False},
                    {'text': '5', 'is_correct': False},
                ]
            },
            {
                'question_text': 'To\'g\'ri burchak necha gradus?',
                'question_type': 'single_choice',
                'points': 2,
                'explanation': 'To\'g\'ri burchak 90 gradus',
                'choices': [
                    {'text': '45°', 'is_correct': False},
                    {'text': '90°', 'is_correct': True},
                    {'text': '180°', 'is_correct': False},
                    {'text': '360°', 'is_correct': False},
                ]
            },
            {
                'question_text': 'Qaysi shakllar to\'rtburchaklar?',
                'question_type': 'multiple_choice',
                'points': 3,
                'explanation': 'Kvadrat va to\'rtburchak to\'rtburchaklar turi',
                'choices': [
                    {'text': 'Kvadrat', 'is_correct': True},
                    {'text': 'To\'rtburchak', 'is_correct': True},
                    {'text': 'Uchburchak', 'is_correct': False},
                    {'text': 'Doira', 'is_correct': False},
                ]
            },
        ]
    }
    
    # Test 3: O'lchovlar
    test3_data = {
        'title': 'Matematika - O\'lchovlar va Vaqt',
        'description': '4-sinf uchun o\'lchovlar va vaqt mavzusida test',
        'subject': 'Matematika',
        'grade': 4,
        'time_limit': 20,
        'questions': [
            {
                'question_text': '1 metr necha santimetr?',
                'question_type': 'single_choice',
                'points': 2,
                'explanation': '1 metr = 100 santimetr',
                'choices': [
                    {'text': '10 sm', 'is_correct': False},
                    {'text': '100 sm', 'is_correct': True},
                    {'text': '1000 sm', 'is_correct': False},
                    {'text': '50 sm', 'is_correct': False},
                ]
            },
            {
                'question_text': '1 kilogramm necha gramm?',
                'question_type': 'single_choice',
                'points': 2,
                'explanation': '1 kilogramm = 1000 gramm',
                'choices': [
                    {'text': '100 g', 'is_correct': False},
                    {'text': '500 g', 'is_correct': False},
                    {'text': '1000 g', 'is_correct': True},
                    {'text': '2000 g', 'is_correct': False},
                ]
            },
            {
                'question_text': '1 soat necha daqiqa?',
                'question_type': 'single_choice',
                'points': 1,
                'explanation': '1 soat = 60 daqiqa',
                'choices': [
                    {'text': '30 daqiqa', 'is_correct': False},
                    {'text': '60 daqiqa', 'is_correct': True},
                    {'text': '90 daqiqa', 'is_correct': False},
                    {'text': '120 daqiqa', 'is_correct': False},
                ]
            },
            {
                'question_text': 'Qaysi o\'lchovlar to\'g\'ri?',
                'question_type': 'multiple_choice',
                'points': 3,
                'explanation': '1 m = 100 sm, 1 kg = 1000 g, 1 soat = 60 daqiqa',
                'choices': [
                    {'text': '1 m = 100 sm', 'is_correct': True},
                    {'text': '1 kg = 1000 g', 'is_correct': True},
                    {'text': '1 soat = 30 daqiqa', 'is_correct': False},
                    {'text': '1 soat = 60 daqiqa', 'is_correct': True},
                ]
            },
        ]
    }
    
    tests_data = [test1_data, test2_data, test3_data]
    
    created_count = 0
    for test_data in tests_data:
        # Test mavjudligini tekshirish
        existing_test = Test.objects.filter(
            title=test_data['title'],
            grade=test_data['grade'],
            subject=test_data['subject']
        ).first()
        
        if existing_test:
            print(f"⚠️  Test allaqachon mavjud: {test_data['title']}")
            continue
        
        # Test yaratish
        test = Test.objects.create(
            title=test_data['title'],
            description=test_data['description'],
            subject=test_data['subject'],
            grade=test_data['grade'],
            created_by=creator,
            time_limit=test_data['time_limit'],
            is_active=True,
            max_attempts=1,
            show_results=True,
            shuffle_questions=False
        )
        
        print(f"✓ Test yaratildi: {test.title}")
        
        # Savollar yaratish
        for i, q_data in enumerate(test_data['questions'], 1):
            question = Question.objects.create(
                test=test,
                question_text=q_data['question_text'],
                question_type=q_data['question_type'],
                points=q_data['points'],
                order=i,
                explanation=q_data.get('explanation', '')
            )
            
            # Variantlar yaratish
            if 'choices' in q_data:
                for choice_data in q_data['choices']:
                    Choice.objects.create(
                        question=question,
                        choice_text=choice_data['text'],
                        is_correct=choice_data['is_correct']
                    )
            
            print(f"  ✓ Savol {i}: {question.question_text[:50]}...")
        
        created_count += 1
        print()
    
    print("="*60)
    print(f"✅ Jami {created_count} ta test yaratildi!")
    print("="*60)

if __name__ == '__main__':
    create_math_tests()

