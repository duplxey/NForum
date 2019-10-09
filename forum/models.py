from django.contrib.auth.models import User
from django.db import models


class Subcategory(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=250)

    class Meta:
        verbose_name_plural = "subcategories"

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

    def __str__(self):
        return self.title


class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    content = models.TextField(max_length=2500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True, blank=True)
    date_edited = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.author.username + ":" + self.content
