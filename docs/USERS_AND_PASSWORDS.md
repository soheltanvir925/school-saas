# Users & Passwords

> ⚠️ SECURITY WARNING: This file contains plaintext credentials.
> Do NOT commit this file to version control. Add `docs/USERS_AND_PASSWORDS.md` to `.gitignore`.
> These are for local development/demo only.

## Superuser (full access to all schools via /admin/)

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Superuser |

## Per-School Users

| Username | Password | School | Role |
|----------|----------|--------|------|
| academy_admin | admin123 | academy | Admin |
| dream_admin | admin123 | dreamacademy | Admin |

## Demo Users (Teachers — all schools, password: `demo123`)

| Username | School | Role |
|----------|--------|------|
| alice.johnson+{school}@school.com | all | Teacher (Math) |
| bob.smith+{school}@school.com | all | Teacher (Physics) |
| carol.williams+{school}@school.com | all | Teacher (English) |
| david.brown+{school}@school.com | all | Teacher (CS) |
| eve.davis+{school}@school.com | all | Teacher (Chemistry) |

## Demo Users (Students — all schools, password: `demo123`)

| Username | School | Role |
|----------|--------|------|
| john.doe+{school}@student.com | all | Student |
| jane.miller+{school}@student.com | all | Student |
| michael.wilson+{school}@student.com | all | Student |
| sarah.moore+{school}@student.com | all | Student |
| james.taylor+{school}@student.com | all | Student |

---

## Commands

Create a superuser:
```bash
python manage.py createsuperuser
```

Reset a password:
```bash
python manage.py changepassword <username>
```

List all users:
```bash
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); [print(f'{u.username} | {u.role} | {u.school}') for u in User.objects.all()]"
```
