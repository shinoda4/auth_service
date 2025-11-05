from django.contrib.auth.models import AbstractUser
from django.db import models


class Permission(models.Model):
    permission_code = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    permission_name = models.CharField(blank=False, null=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.permission_code

    class Meta:
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"


class Role(models.Model):
    role_name = models.CharField(blank=False, null=False)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.role_name

    class Meta:
        proxy = False


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    roles = models.ManyToManyField(Role, blank=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

    class Meta:
        proxy = False
