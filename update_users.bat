@echo off
cd /d C:\Users\Admin\Desktop\school_saas
call venv\Scripts\activate
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); updated = User.objects.filter(school__isnull=False, is_superuser=True).update(is_superuser=False); print(f'Updated {updated} school-level users'); print('Done!')"
pause
