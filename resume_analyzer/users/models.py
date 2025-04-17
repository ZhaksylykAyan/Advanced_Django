from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('JOB_SEEKER', 'Job Seeker'),
        ('RECRUITER', 'Recruiter'),
        ('ADMIN', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='JOB_SEEKER')

    def __str__(self):
        return f"{self.username} ({self.role})"
