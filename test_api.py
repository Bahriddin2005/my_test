#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mytest.settings')
django.setup()

from django.test import Client
from accounts.models import User
import json

client = Client()
admin = User.objects.filter(role='admin').first()

if admin:
    client.force_login(admin)
    response = client.get('/tests/', HTTP_ACCEPT='application/json')
    data = json.loads(response.content)
    
    print(f'Status: {response.status_code}')
    print(f'Tests count: {len(data.get("tests", []))}')
    print(f'User role: {data.get("user_role")}')
    print('\nTestlar:')
    for t in data.get('tests', [])[:10]:
        print(f'- {t["title"]} (Grade: {t["grade"]}, Active: {t["is_active"]}, Subject: {t["subject"]})')
else:
    print('Admin topilmadi')

