# Generated by Django 3.0.5 on 2020-04-04 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0015_auto_20200404_1139'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thread',
            name='locked',
        ),
        migrations.RemoveField(
            model_name='thread',
            name='locked_by',
        ),
        migrations.AlterField(
            model_name='thread',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
