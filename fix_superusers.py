#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Update school-level users to not be superuser
updated = User.objects.filter(school__isnull=False, is_superuser=True).update(is_superuser=False)
print(f'Updated {updated} school-level users to is_superuser=False')

# Show current state
print('\nCurrent users:')
for user in User.objects.all().values('username', 'school__name', 'is_superuser', 'is_staff'):
    print(f"  {user['username']}: school={user['school__name']}, is_superuser={user['is_superuser']}, is_staff={user['is_staff']}")
