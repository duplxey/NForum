from django.contrib.auth.models import User
from django.db import models

from forum.models import Message, Thread


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=750, default="Another cool user.")
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars/')

    # ---------------------------------------------------------
    # > Alerts
    # ---------------------------------------------------------
    def get_alerts(self):
        return Alert.objects.filter(user=self.user)

    def get_unseen_alerts(self):
        return Alert.objects.filter(user=self.user).filter(seen__isnull=True)

    # ---------------------------------------------------------
    # > Achievements
    # ---------------------------------------------------------
    def get_unlocked_achievements(self):
        return UserAchievement.objects.filter(user=self.user)

    def get_locked_achievements(self):
        return Achievement.objects.exclude(userachievement__user=self.user)

    def check_add_achievements(self, criteria):
        locked_achievements = self.get_locked_achievements().filter(criteria=criteria)

        # If the user already unlocked all the achievements, let's avoid executing additional queries
        if locked_achievements.count() == 0:
            return False

        # No switch statement in python? Makes me kinda sad :(
        value = 0
        if criteria == Achievement.POST_COUNT:
            value = self.get_post_count()
        elif criteria == Achievement.THREAD_COUNT:
            value = self.get_thread_count()
        elif criteria == Achievement.UPVOTE_COUNT:
            value = self.get_upvote_count()
        elif criteria == Achievement.DOWNVOTE_COUNT:
            value = self.get_downvote_count()

        for locked_achievement in locked_achievements:
            if value >= locked_achievement.value:
                user_achievement = UserAchievement(user=self.user, achievement=locked_achievement)
                user_achievement.save()

                Alert.objects.create(user=self.user, type=Alert.ACHIEVEMENT)
                return True
        return False

    # ---------------------------------------------------------
    # > Forum statistics
    # ---------------------------------------------------------
    def get_thread_count(self):
        return Thread.objects.filter(author=self.user).count()

    def get_post_count(self):
        return Message.objects.filter(author=self.user).count()

    # ---------------------------------------------------------
    # > Reputation
    # ---------------------------------------------------------
    @staticmethod
    def get_reputation_ordered_user_list():
        unsorted = User.objects.all()
        a = sorted(unsorted, key=lambda t: -t.userprofile.get_reputation())
        return a

    def get_reputation(self):
        return self.get_upvote_count() - self.get_downvote_count()

    def get_upvote_count(self):
        a = 0
        for message in Message.objects.filter(author=self.user):
            a += message.upvoters.count()
        return a

    def get_downvote_count(self):
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

    class Meta:
        ordering = ["-datetime"]

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

    def __str__(self):
        return self.name + " (" + self.description + ")"


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ["-datetime"]

    def __str__(self):
        return self.user.username + " (" + self.achievement.name + ")"

