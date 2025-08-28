from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ("user", "User"),
        ("manager", "Manager"),
        ("admin", "Admin"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")

    def __str__(self):
        return self.username

