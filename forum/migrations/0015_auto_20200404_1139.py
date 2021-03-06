# Generated by Django 3.0.5 on 2020-04-04 09:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0014_forumconfiguration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='forumconfiguration',
            options={'verbose_name': 'Forum configuration'},
        ),
        migrations.AddField(
            model_name='thread',
            name='locked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='thread',
            name='locked_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='locked_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='thread',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tauthor', to=settings.AUTH_USER_MODEL),
        ),
    ]
