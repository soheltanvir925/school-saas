from django.core.management.base import BaseCommand
from django.db import connections
from core.models import School
from core.utils import set_current_db_name
from schools.models import Teacher, Student


class Command(BaseCommand):
    help = 'Populates Academy school with demo teachers and students'

    def handle(self, *args, **kwargs):
        try:
            academy_default = School.objects.get(subdomain='academy')
            db_name = academy_default.database_name
            
            # Configure connection if needed
            if db_name not in connections.databases:
                new_db_config = connections.databases['default'].copy()
                new_db_config['NAME'] = db_name
                connections.databases[db_name] = new_db_config
                
            # Set the current DB for the router
            set_current_db_name(db_name)

            # Ensure academy school exists in tenant DB for FK constraints
            if not School.objects.using(db_name).filter(id=academy_default.id).exists():
                academy_default.save(using=db_name)
                self.stdout.write(f"Synced school {academy_default.name} to {db_name}")
            
            # Re-fetch academy from the tenant DB to avoid cross-database relation errors
            academy_tenant = School.objects.using(db_name).get(id=academy_default.id)

        except School.DoesNotExist:
            self.stdout.write(self.style.ERROR('School "academy" not found.'))
            return

        # 1. Create 5 Teachers
        self.stdout.write('Creating teachers...')
        teacher_names = [
            ('John', 'Doe', 'Mathematics'),
            ('Jane', 'Smith', 'Science'),
            ('Robert', 'Brown', 'History'),
            ('Emily', 'Davis', 'English'),
            ('Michael', 'Wilson', 'Physics')
        ]
        
        for first, last, spec in teacher_names:
            Teacher.objects.using(db_name).update_or_create(
                email=f"{first.lower()}_{last.lower()}@example.com",
                defaults={
                    'school': academy_tenant,
                    'first_name': first,
                    'last_name': last,
                    'bio': f"Experienced {spec} teacher.",
                    'specialization': spec
                }
            )
            self.stdout.write(f"Created teacher: {first} {last}")

        # 2. Create 5 Students
        self.stdout.write('Creating students...')
        student_names = [
            ('Alice', 'Johnson'),
            ('Bob', 'Miller'),
            ('Charlie', 'Garcia'),
            ('David', 'Martinez'),
            ('Eve', 'Rodriguez')
        ]
        
        for i, (first, last) in enumerate(student_names, 1):
            Student.objects.using(db_name).update_or_create(
                email=f"{first.lower()}_{last.lower()}@example.com",
                defaults={
                    'school': academy_tenant,
                    'first_name': first,
                    'last_name': last,
                    'roll_number': f"ACAD-2026-{i:03d}",
                    'father_name': f"Father of {first}",
                    'mother_name': f"Mother of {first}"
                }
            )
            self.stdout.write(f"Created student: {first} {last}")

        self.stdout.write(self.style.SUCCESS('Successfully populated Academy school with 5 teachers and 5 students.'))
