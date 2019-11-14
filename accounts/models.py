import datetime

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


class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    MENTION = 'ME'
    RESPOND = 'RE'
    UPVOTE = 'UP'
    DOWNVOTE = 'DO'
    ACHIEVEMENT = 'AC'
    ALERT_TYPES = [
        (MENTION, 'Mention'),
        (RESPOND, 'Respond'),
        (UPVOTE, 'Upvote'),
        (DOWNVOTE, 'Downvote'),
        (ACHIEVEMENT, 'Achievement'),
    ]
    type = models.CharField(max_length=2, choices=ALERT_TYPES, default=MENTION)
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
    seen = models.DateTimeField(null=True, blank=True)
    caused_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='caused_by')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(max_length=300, null=True, blank=True)

    @staticmethod
    def get_latest_alerts(user, amount):
        return Alert.objects.filter(user=user).order_by('-datetime')[:amount]

    @staticmethod
    def get_unseen_alerts(user):
        return Alert.objects.filter(user=user).filter(seen__isnull=True)

    @staticmethod
    def clear_unseen_alerts(user):
        for alert in Alert.get_unseen_alerts(user):
            alert.seen = datetime.datetime.now()
            alert.save()

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
    def check_add_achievements(user, criteria):
        locked_achievements = Achievement.get_locked_achievements(user).filter(criteria=criteria)

        # If the user already has all the achievements, let's avoid executing additional queries
        if locked_achievements.count() == 0:
            return False

        # No switch statement in python? Makes me kinda sad :(
        value = 0
        if criteria == Achievement.POST_COUNT:
            value = Message.objects.filter(author=user).count()
        elif criteria == Achievement.THREAD_COUNT:
            value = Thread.objects.filter(author=user).count()
        elif criteria == Achievement.UPVOTE_COUNT:
            value = Profile.get_profile(user).get_upvotes()
        elif criteria == Achievement.DOWNVOTE_COUNT:
            value = Profile.get_profile(user).get_downvotes()

        for locked_achievement in locked_achievements:
            if value >= locked_achievement.value:
                user_achievement = UserAchievement(user=user, achievement=locked_achievement)
                user_achievement.save()

                alert = Alert(user=user, type=Alert.ACHIEVEMENT)
                alert.save()

                return True

        return False

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

    def __str__(self):
        return self.user.username + " (" + self.achievement.name + ")"

