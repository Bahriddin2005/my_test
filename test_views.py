#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mytest.settings')
django.setup()

from accounts.models import User
from tests_app.models import Test
from django.db import connection
import json

# Admin foydalanuvchisini topish
admin = User.objects.filter(role='admin').first()

if not admin:
    print('Admin topilmadi')
    sys.exit(1)

print(f'Admin: {admin.username}')
print('='*60)

# Raw SQL yordamida test ID'larni olish
test_ids = []
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM tests_app_test ORDER BY created_at DESC")
        test_ids = [row[0] for row in cursor.fetchall()]
except Exception as db_error:
    print(f'Error fetching test IDs: {db_error}')
    test_ids = []

print(f'Test IDs found: {len(test_ids)}')
print(f'Test IDs: {test_ids}')

# Test obyektlarini yuklash
tests = []
for test_id in test_ids:
    try:
        test = Test.objects.select_related('created_by').get(id=test_id)
        tests.append(test)
    except Exception as e:
        print(f'Error loading test {test_id}: {e}')
        continue

print(f'\nLoaded tests: {len(tests)}')
for test in tests:
    print(f'- {test.title} (ID: {test.id}, Grade: {test.grade}, Subject: {test.subject}, Active: {test.is_active})')

# Test ma'lumotlarini formatlash
test_data = []
for test in tests:
    try:
        from tests_app.models import TestAttempt
        attempt_count = TestAttempt.objects.filter(test=test, is_completed=True).count()
        test_data.append({
            'id': test.id,
            'title': test.title,
            'subject': test.subject,
            'description': test.description or '',
            'grade': test.grade,
            'total_questions': test.total_questions,
            'is_active': test.is_active,
            'created_at': test.created_at.isoformat() if test.created_at else '',
            'created_by': test.created_by.get_full_name() if test.created_by and hasattr(test.created_by, 'get_full_name') else (test.created_by.username if test.created_by else 'Noma\'lum'),
            'attempt_count': attempt_count,
            'max_attempts': test.max_attempts,
            'time_limit': test.time_limit,
        })
    except Exception as e:
        print(f'Error processing test {test.id}: {e}')
        continue

print(f'\nFormatted test data: {len(test_data)}')
for td in test_data:
    print(f'- {td["title"]} (Grade: {td["grade"]}, Subject: {td["subject"]})')

print('\n' + '='*60)
print('Testlar mavjud va to\'g\'ri formatlangan!')

