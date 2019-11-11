from django.contrib.auth.models import User
from django.db import models

from forum.models import Message


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

    def get_upvotes(self):
        a = 0
        for message in Message.objects.filter(author=self.user):
            a += message.upvoters.count()
        return a

    def get_downvotes(self):
        a = 0
        for message in Message.objects.filter(author=self.user):
            a += message.downvoters.count()
        return a

    def __str__(self):
        return self.user.username + "'s profile"
