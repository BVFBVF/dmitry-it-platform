from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        MENTOR = 'mentor', 'Mentor'
        VIEWER = 'viewer', 'Viewer'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.VIEWER,
    )

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    @property
    def is_mentor(self):
        return self.role == self.Role.MENTOR

    @property
    def is_viewer(self):
        return self.role == self.Role.VIEWER
