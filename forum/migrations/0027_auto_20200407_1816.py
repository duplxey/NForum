# Generated by Django 3.0.5 on 2020-04-07 16:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0026_auto_20200407_1804'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='subcategories',
        ),
        migrations.AddField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='forum.Category'),
            preserve_default=False,
        ),
    ]
