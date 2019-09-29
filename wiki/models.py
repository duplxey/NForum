from django.db import models
from django.utils import timezone
from tinymce import HTMLField


class WikiPage(models.Model):
    display_index = models.IntegerField()
    url = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    content = HTMLField('Content')
    # TODO: add the author
    # TODO: add the editors
    created_datetime = models.DateTimeField(default=timezone.now)
    edited_datetime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
