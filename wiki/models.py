from django.db import models
from django.utils import timezone


class WikiPage(models.Model):
    display_index = models.IntegerField()
    title = models.CharField(max_length=64)
    content = models.TextField(max_length=2500)
    # TODO: add the author
    # TODO: add the editors
    created_datetime = models.DateTimeField(default=timezone.now)
    edited_datetime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
