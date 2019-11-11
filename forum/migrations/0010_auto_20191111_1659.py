# Generated by Django 2.2.5 on 2019-11-11 15:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0009_auto_20191009_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='downvoters',
            field=models.ManyToManyField(blank=True, related_name='upvoters', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='upvoters',
            field=models.ManyToManyField(blank=True, related_name='downvoters', to=settings.AUTH_USER_MODEL),
        ),
    ]