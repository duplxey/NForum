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


class SiteColorPalette(SingletonModel):
    special_color = models.CharField(max_length=6, default="2E86AB")
    special_dark_color = models.CharField(max_length=6, default="065A82")

    background = models.CharField(max_length=6, default="FFFFFF")
    background_gray = models.CharField(max_length=6, default="F3F3F3")
    background_dark = models.CharField(max_length=6, default="2d2d2d")

    link = models.CharField(max_length=6, default="007BFF")
    link_hover = models.CharField(max_length=6, default="0056B3")

    text_color = models.CharField(max_length=6, default="282828")
    text_color_hover = models.CharField(max_length=6, default="232323")
    text_color_light = models.CharField(max_length=6, default="ffffff")
    text_color_light_hover = models.CharField(max_length=6, default="F3EFF5")

    def __str__(self):
        return "Site color palette"

    class Meta:
        verbose_name = "Site color palette"


class SiteSocialNetwork(models.Model):
    name = models.CharField(max_length=32)
    url = models.CharField(max_length=255)
    fa_icon = models.CharField(max_length=64)

    def __str__(self):
        return self.name
