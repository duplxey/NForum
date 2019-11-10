from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=300, default="Another cool user.")
    last_action = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to='images/')

    @staticmethod
    def get_profile(user):
        return Profile.objects.get(user=user)

    @staticmethod
    def get_registered_user_count():
        return Profile.objects.all().count()

    @staticmethod
    def get_active_user_count():
        return 0

    def __str__(self):
        return self.user.username + "'s profile"
