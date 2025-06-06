# apps/accounts/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from apps.accounts.profiles.user.models.user_profile import UserProfile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Yangi foydalanuvchi yaratildi (created=True) va uning roli 'user' bo'lsa,
    unga mos UserProfile yaratamiz.
    """
    if created and instance.role == 'user':  # 'user' kichik harflarda yozilishi kerak
        UserProfile.objects.create(user=instance)
