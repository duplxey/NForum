from django.contrib.auth.models import User
from django.db import models

from forum.models import Message, Thread


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


class AlertType(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)
    description = models.TextField(max_length=300, null=False, blank=True)

    def __str__(self):
        return self.name


class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.OneToOneField(AlertType, on_delete=models.CASCADE)
    caused_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='caused_by')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(max_length=300)

    def __str__(self):
        return self.message
