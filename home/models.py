from django.db import models
from solo.models import SingletonModel


class SiteConfiguration(SingletonModel):
    name = models.CharField(max_length=255, default="Site Name")
    description = models.TextField(max_length=750, default="Site Description")
    description_short = models.TextField(max_length=128, default="Site Short Description")
    logo = models.ImageField(null=True, blank=True)
    maintenance_mode = models.BooleanField(default=False)

    def __str__(self):
        return "Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"


class SiteSocialNetwork(models.Model):
    name = models.CharField(max_length=32)
    url = models.CharField(max_length=255)
    fa_icon = models.CharField(max_length=64)

    def __str__(self):
        return self.name
