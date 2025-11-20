# Migration Instructions

## Problem
The error `no such column: tests_app_test.is_paused` occurs because the migration `0006_test_is_paused_test_paused_at.py` has not been run on the production server.

## Solution
Run the migration on the production server:

```bash
# SSH into your production server
ssh user@your-server

# Navigate to your project directory
cd /home/baxadev/my_test

# Activate virtual environment
source venv/bin/activate

# Run migrations
python manage.py migrate tests_app

# Or run all migrations
python manage.py migrate
```

## Verify Migration
After running the migration, verify that the columns exist:

```bash
# For SQLite (if using SQLite)
sqlite3 db.sqlite3 "PRAGMA table_info(tests_app_test);"

# For PostgreSQL (if using PostgreSQL)
psql -d your_database -c "\d tests_app_test"
```

You should see `is_paused` and `paused_at` columns in the output.

## Alternative: Run via Django Shell
If you have access to Django shell on production:

```python
from django.core.management import call_command
call_command('migrate', 'tests_app')
```

## Important Notes
- Make sure to backup your database before running migrations
- The migration adds two new fields with default values, so existing data will be safe
- After migration, restart your web server (if needed)

