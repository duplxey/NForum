# Generated by Django 2.2.5 on 2019-10-16 18:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0005_auto_20191016_2033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wikipage',
            name='editors',
        ),
        migrations.AlterField(
            model_name='wikipage',
            name='last_editor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='last_editor', to=settings.AUTH_USER_MODEL),
        ),
    ]
