from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import UserProfile


@receiver(post_save, sender=User)
def post_save(sender, instance, created, raw, using, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, avatar="images/user.png")


# @receiver(post_save, sender=Message)
# def post_save(sender, instance, created, raw, using, **kwargs):
#     if created:
#         Achievement.check_add_achievements(instance.author, Achievement.POST_COUNT)


# @receiver(post_save, sender=Thread)
# def thread_save(sender, instance, created, raw, using, **kwargs):
#     if created:
#         Achievement.check_add_achievements(instance.author, Achievement.THREAD_COUNT)
