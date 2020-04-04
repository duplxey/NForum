from django.contrib.auth.models import User
from django.db import models
from tinymce import HTMLField


class WikiPage(models.Model):
    display_index = models.IntegerField(unique=True)
    title = models.CharField(max_length=64, unique=True)
    url = models.SlugField(max_length=64, unique=True)
    content = HTMLField('Content', max_length=5000)
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='author')
    last_editor = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='last_editor')
    created_datetime = models.DateTimeField(auto_now_add=True)
    edited_datetime = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['display_index']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        # To keep display_indexes in boundaries
        highest = WikiPage.objects.count() + 5
        if self.display_index > highest:
            self.display_index = highest

        super().save(force_insert, force_update, using, update_fields)

    def get_next_page(self):
        try:
            return WikiPage.objects.get(display_index=self.display_index + 1)
        except WikiPage.DoesNotExist:
            return None

    def get_previous_page(self):
        try:
            return WikiPage.objects.get(display_index=self.display_index - 1)
        except WikiPage.DoesNotExist:
            return None

    def __str__(self):
        return self.title
