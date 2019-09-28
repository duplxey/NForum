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
