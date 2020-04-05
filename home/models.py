from django.db import models
from solo.models import SingletonModel


class SiteConfiguration(SingletonModel):
    name = models.CharField(max_length=255, default="Site Name")
    description = models.TextField(max_length=750, default="Site Description")
    description_short = models.TextField(max_length=128, default="Site Short Description")
    keywords = models.TextField(max_length=750, default="keyword1, keyword2, keyword3, keyword4")
    favicon = models.ImageField(null=True, blank=True)
    logo = models.ImageField(null=True, blank=True)

    def __str__(self):
        return "Site configuration"

    class Meta:
        verbose_name = "Site configuration"


class SiteSocialNetwork(models.Model):
    name = models.CharField(max_length=32)
    url = models.CharField(max_length=255)
    fa_icon = models.CharField(max_length=64)

    def __str__(self):
        return self.name
