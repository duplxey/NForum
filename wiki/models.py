from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from tinymce import HTMLField


class WikiPage(models.Model):
    display_index = models.IntegerField(unique=True)
    title = models.CharField(max_length=64, unique=True)
    url = models.CharField(max_length=64, unique=True)
    content = HTMLField('Content', max_length=5000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    last_editor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='last_editor', null=True, blank=True)
    created_datetime = models.DateTimeField(default=timezone.now)
    edited_datetime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
