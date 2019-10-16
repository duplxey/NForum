# Generated by Django 2.2.5 on 2019-10-16 18:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wiki', '0004_auto_20190929_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='wikipage',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wikipage',
            name='editors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='wikipage',
            name='last_editor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='last_editor', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='wikipage',
            name='content',
            field=tinymce.models.HTMLField(max_length=5000, verbose_name='Content'),
        ),
        migrations.AlterField(
            model_name='wikipage',
            name='url',
            field=models.CharField(default='djangodbmodelsfieldsCharField', max_length=64),
        ),
    ]
