from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_save, sender=User)
def post_save(sender, instance, created, raw, using, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
