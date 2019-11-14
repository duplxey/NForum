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

    def get_unseen_alerts(self):
        return Alert.objects.filter(user=self.user).filter(seen__isnull=True).count()

    def __str__(self):
        return self.user.username + "'s profile"


class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    MENTION = 'ME'
    RESPOND = 'RE'
    ALERT_TYPES = [
        (MENTION, 'Mention'),
        (RESPOND, 'Respond'),
    ]
    type = models.CharField(max_length=2, choices=ALERT_TYPES, default=MENTION)
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
    seen = models.DateTimeField(null=True, blank=True)
    caused_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='caused_by')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.user.username + " (" + self.type + ")"


class Achievement(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=300, blank=True, null=True)
    POST_COUNT = 'PC'
    THREAD_COUNT = 'TC'
    UPVOTE_COUNT = 'UP'
    DOWNVOTE_COUNT = 'DO'
    CRITERIAS = [
        (POST_COUNT, 'Post count'),
        (THREAD_COUNT, 'Thread count'),
        (UPVOTE_COUNT, 'Upvotes'),
        (DOWNVOTE_COUNT, 'Downvotes'),
    ]
    criteria = models.CharField(max_length=2, choices=CRITERIAS, default=POST_COUNT)
    value = models.IntegerField(blank=False, null=False)

    @staticmethod
    def get_unlocked_achievements(user):
        return UserAchievement.objects.filter(user=user).order_by('-datetime')

    @staticmethod
    def get_locked_achievements(user):
        return Achievement.objects.exclude(userachievement__user=user)

    def __str__(self):
        return self.name + " (" + self.description + ")"


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
