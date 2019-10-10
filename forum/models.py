from django.contrib.auth.models import User
from django.db import models


class Subcategory(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=250)

    class Meta:
        verbose_name_plural = "subcategories"

    def get_latest_thread(self):
        latest_thread = None
        latest_thread_date = None
        for thread in Thread.objects.filter(subcategory=self):
            first_message = Message.objects.filter(thread=thread).order_by('date_posted')[0]
            if latest_thread_date is None or first_message.date_posted > latest_thread_date:
                latest_thread = thread
                latest_thread_date = first_message.date_posted
        return latest_thread

    def get_thread_count(self):
        return Thread.objects.filter(subcategory=self).count()

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
        return Message.objects.filter(thread=self)

    def get_first_message(self):
        return self.get_messages().order_by('date_posted')[0]

    def get_last_message(self):
        return self.get_messages().order_by('-date_posted')[0]

    def get_message_count(self):
        return self.get_messages().count()

    def __str__(self):
        return self.title + " by " + self.author.username


class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    content = models.TextField(max_length=2500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True, blank=True)
    date_edited = models.DateTimeField(null=True, blank=True)

    @staticmethod
    def get_recent_messages(amount):
        return Message.objects.all().order_by('-date_posted')[:amount]

    @staticmethod
    def get_message_count():
        return Message.objects.all().count()

    def __str__(self):
        return self.author.username + ":" + self.content
