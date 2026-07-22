from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    school = models.ForeignKey('core.School', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='admin')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
