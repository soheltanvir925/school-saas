from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import School

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates main superuser and school superusers for academy and dreamacademy'

    def handle(self, *args, **kwargs):
        # 1. Main Superuser
        self.create_user('admin', None, 'Main Superuser')

        # 2. Academy School Superuser
        self.create_user('academy_admin', 'academy', 'Academy Superuser')

        # 3. DreamAcademy School Superuser
        self.create_user('dream_admin', 'dreamacademy', 'DreamAcademy Superuser')

    def create_user(self, username, subdomain, label):
        password = 'admin123'
        school = None
        is_main_superuser = not subdomain
        if subdomain:
            try:
                school = School.objects.get(subdomain=subdomain)
            except School.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'School with subdomain "{subdomain}" not found.'))
                return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'is_superuser': is_main_superuser,
                'is_staff': True,
                'school': school,
                'role': 'admin'
            }
        )
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully created {label}: {username} (Password: {password})'))
        else:
            self.stdout.write(self.style.WARNING(f'{label} already exists: {username}'))
