from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.db import connections
from core.models import School
from core.utils import set_current_db_name
from schools.models import Teacher
from users.models import User


class Command(BaseCommand):
    help = 'Creates User accounts for existing teachers without one'

    def handle(self, *args, **kwargs):
        schools = School.objects.all()

        for school in schools:
            db_name = school.database_name
            if db_name not in connections:
                new_db_config = connections.databases['default'].copy()
                new_db_config['NAME'] = db_name
                connections.databases[db_name] = new_db_config

            set_current_db_name(db_name)

            teachers = Teacher.objects.filter(school=school)
            created = 0
            for teacher in teachers:
                if not teacher.email:
                    continue
                if not User.objects.filter(username=teacher.email).exists():
                    User.objects.create(
                        username=teacher.email,
                        email=teacher.email,
                        first_name=teacher.first_name or '',
                        last_name=teacher.last_name or '',
                        password=make_password('teacher123'),
                        school=school,
                        role='teacher',
                    )
                    created += 1
                    self.stdout.write(f"Created user for {teacher.email}")

            self.stdout.write(self.style.SUCCESS(
                f"{school.name}: created {created} teacher user(s)"
            ))
