#!/bin/bash
# Virtual environmentni faollashtirish va Django serverni ishga tushirish

cd "$(dirname "$0")"
source venv/bin/activate
echo "Virtual environment faollashtirildi: $(which python)"
echo "Django serverni ishga tushirish..."
python manage.py runserver

