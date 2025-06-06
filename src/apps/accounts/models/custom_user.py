from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class UserRole(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    USER = 'user', 'User'

class CustomUserManager(BaseUserManager):
    def create_user(self, username_email, password=None, **extra_fields):
        if not username_email:
            raise ValueError('Foydalanuvchi nomi yoki email kiritilishi kerak.')
        user = self.model(username_email=username_email, role=UserRole.USER, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username_email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(
            username_email=username_email,
            password=password,
            **extra_fields  # faqat shu yerda bering, is_staff alohida bermang
        )


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username_email = models.CharField(max_length=255, unique=True)
    role = models.CharField(max_length=10, choices=UserRole.choices, default=UserRole.USER)
    created_at = models.DateTimeField(default=timezone.now)
    reset_password_email = models.EmailField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username_email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username_email

