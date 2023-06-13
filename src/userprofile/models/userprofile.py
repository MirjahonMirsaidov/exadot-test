from django.contrib.auth.models import AbstractUser
from django.db import models

from userprofile.manager import ProfileManager


class RoleChoices(models.TextChoices):
    ADMIN = 'admin'
    VENDOR = 'vendor'
    USER = 'user'


class UserProfile(AbstractUser):
    """ Profile (custom User ) model """
    role = models.CharField(max_length=256, choices=RoleChoices.choices, default=RoleChoices.USER)

    # model manager
    objects = ProfileManager()

    def __str__(self):
        return self.email

    class Meta:
        ordering = ('-date_joined',)
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        db_table = "profile"




