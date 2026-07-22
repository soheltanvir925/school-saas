from django.core.management.base import BaseCommand
from django.db import connections
from django.conf import settings
from django.utils import timezone
from datetime import date, timedelta
import random

from core.models import School
from core.utils import set_current_db_name, clear_current_db_name
from schools.models import FeeCategory, FeeStructure, FeePayment, Student


FEE_CATEGORIES = [
    {"name": "Tuition", "description": "Regular tuition fees"},
    {"name": "Library", "description": "Library and resource fees"},
    {"name": "Sports", "description": "Sports and extracurricular fees"},
    {"name": "Transport", "description": "School transport fees"},
    {"name": "Laboratory", "description": "Science lab fees"},
    {"name": "Development", "description": "Infrastructure development fees"},
]

FEE_STRUCTURES = [
    {"name": "Monthly Tuition", "category": "Tuition", "amount": 250.00, "frequency": "monthly", "due_day": 10},
    {"name": "Annual Library Fee", "category": "Library", "amount": 80.00, "frequency": "yearly", "due_day": 15},
    {"name": "Sports Fee", "category": "Sports", "amount": 50.00, "frequency": "monthly", "due_day": 10},
    {"name": "Transport Fee", "category": "Transport", "amount": 120.00, "frequency": "monthly", "due_day": 5},
    {"name": "Lab Fee", "category": "Laboratory", "amount": 60.00, "frequency": "quarterly", "due_day": 20},
    {"name": "Development Fee", "category": "Development", "amount": 200.00, "frequency": "yearly", "due_day": 1},
]

PAYMENT_METHODS = ["cash", "check", "bank", "online"]
STATUSES = ["paid", "paid", "paid", "paid", "partial", "pending"]


def configure_db(db_name):
    if db_name not in connections:
        cfg = connections.databases['default'].copy()
        cfg['NAME'] = db_name
        connections.databases[db_name] = cfg


class Command(BaseCommand):
    help = 'Seeds demo fee data (categories, structures, payments) for all schools'

    def handle(self, *args, **options):
        today = date.today()
        schools = School.objects.filter(is_active=True)

        default_db = connections.databases['default']['NAME']

        for school in schools:
            db_name = school.database_name

            # Skip schools whose db is the default DB (tenant tables not migrated there)
            if db_name == default_db:
                self.stdout.write(self.style.WARNING(
                    f"  Skipping {school.name} (db='{db_name}' is default DB, no tenant tables)"
                ))
                continue

            configure_db(db_name)
            set_current_db_name(db_name)

            self.stdout.write(f"\n=== {school.name} (DB: {db_name}) ===")

            # Sync school record into tenant DB
            if not School.objects.using(db_name).filter(id=school.id).exists():
                school.save(using=db_name)

            school_tenant = School.objects.using(db_name).get(id=school.id)

            # Create Fee Categories
            cat_map = {}
            for fc in FEE_CATEGORIES:
                obj, created = FeeCategory.objects.using(db_name).update_or_create(
                    school=school_tenant,
                    name=fc["name"],
                    defaults={"description": fc["description"]},
                )
                cat_map[fc["name"]] = obj
                if created:
                    self.stdout.write(f"  + Category: {fc['name']}")

            # Create Fee Structures
            struct_map = {}
            for fs in FEE_STRUCTURES:
                obj, created = FeeStructure.objects.using(db_name).update_or_create(
                    school=school_tenant,
                    name=fs["name"],
                    defaults={
                        "fee_category": cat_map[fs["category"]],
                        "amount": fs["amount"],
                        "frequency": fs["frequency"],
                        "due_day": fs["due_day"],
                        "is_active": True,
                    },
                )
                struct_map[fs["name"]] = obj
                if created:
                    self.stdout.write(f"  + Structure: {fs['name']} (${fs['amount']})")

            # Create Fee Payments for students
            students = Student.objects.using(db_name).filter(school=school_tenant)
            if not students.exists():
                self.stdout.write("  No students found, skipping payments")
                continue

            for student in students:
                # Pick 3-5 random fee structures for this student
                num_structures = random.randint(3, 5)
                selected = random.sample(list(struct_map.values()), num_structures)

                for fs_obj in selected:
                    # Generate 2-4 historical payments per structure
                    num_payments = random.randint(2, 4)
                    for i in range(num_payments):
                        months_ago = i * random.choice([1, 2, 3])
                        pay_date = today - timedelta(days=months_ago * 30 + random.randint(0, 15))
                        if pay_date > today:
                            pay_date = today

                        status = random.choice(STATUSES)
                        if status == "paid":
                            amount = fs_obj.amount
                        elif status == "partial":
                            amount = round(fs_obj.amount * random.uniform(0.3, 0.9), 2)
                        else:
                            amount = 0.0

                        method = random.choice(PAYMENT_METHODS)
                        txn_id = f"TXN-{school.id}-{student.id}-{fs_obj.id}-{i}"

                        existing = FeePayment.objects.using(db_name).filter(
                            transaction_id=txn_id
                        ).first()
                        if existing:
                            continue

                        FeePayment.objects.using(db_name).create(
                            school=school_tenant,
                            student=student,
                            fee_structure=fs_obj,
                            amount_paid=amount or fs_obj.amount,
                            payment_date=pay_date,
                            payment_method=method,
                            transaction_id=txn_id,
                            status=status if amount > 0 else "pending",
                            remarks=f"Demo payment for {fs_obj.name}",
                        )

            self.stdout.write(f"  Created payments for {students.count()} students")
            clear_current_db_name()

        self.stdout.write(self.style.SUCCESS("\nDone! Demo fee data seeded successfully."))
