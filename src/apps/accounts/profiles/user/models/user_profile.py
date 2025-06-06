# apps/accounts/models.py

from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # boshqa profil uchun maydonlar

    def __str__(self):
        return f'Profile for {self.user.username_email}'
