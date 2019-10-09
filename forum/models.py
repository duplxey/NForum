from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class Subcategory(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=250)

    class Meta:
        verbose_name_plural = "subcategories"

    def get_latest_thread(self):
        latest_thread = None
        dt = now()
        for thread in Thread.objects.filter(subcategory=self):
            message = Message.objects.filter(thread=thread).order_by('date_posted')[0]
            if message.date_posted < dt:
                latest_thread = thread
                dt = message.date_posted
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

    def get_message_count(self):
        return Message.objects.filter(thread=self).count()

    def __str__(self):
        return self.title + " by " + self.author.username


class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    content = models.TextField(max_length=2500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True, blank=True)
    date_edited = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.author.username + ":" + self.content
