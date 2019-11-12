from django.contrib.auth.models import User
from django.db import models


class Subcategory(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=250)

    class Meta:
        verbose_name_plural = "subcategories"

    def get_threads(self):
        return Thread.objects.all().filter(subcategory=self)

    def get_thread_count(self):
        return Thread.objects.filter(subcategory=self).count()

    def get_latest_thread(self):
        for message in Message.objects.all().order_by("-date_posted"):
            if message.thread.subcategory == self:
                return message.thread

    def get_message_count(self):
        message_count = 0
        for thread in Thread.objects.filter(subcategory=self):
            message_count = message_count + thread.get_message_count()
        return message_count

    def __str__(self):
        return self.title + " (" + self.description + ")"


class Category(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=250)
    subcategories = models.ManyToManyField(Subcategory, blank=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title + " (" + self.description + ")"


class Thread(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)

    @staticmethod
    def get_thread_count():
        return Thread.objects.all().count()

    def get_messages(self):
        return Message.objects.filter(thread=self).order_by('pk')

    def get_first_message(self):
        return self.get_messages().order_by('date_posted')[0]

    def get_last_message(self):
        return self.get_messages().order_by('-date_posted')[0]

    def get_message_count(self):
        return self.get_messages().count()

    def get_participants(self):
        participants = set()
        for message in self.get_messages():
            participants.add(message.author)
        return participants

    def __str__(self):
        return self.title + " by " + self.author.username


class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    content = models.TextField(max_length=2500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True, blank=True)
    date_edited = models.DateTimeField(null=True, blank=True)
    upvoters = models.ManyToManyField(User, blank=True, related_name='downvoters')
    downvoters = models.ManyToManyField(User, blank=True, related_name='upvoters')

    @staticmethod
    def get_recent_messages(amount):
        return Message.objects.all().order_by('-date_posted')[:amount]

    @staticmethod
    def get_message_count():
        return Message.objects.all().count()

    def is_upvoter(self, user):
        return user in self.upvoters.all()

    def is_downvoter(self, user):
        return user in self.downvoters.all()

    def __str__(self):
        return self.author.username + ":" + self.content
