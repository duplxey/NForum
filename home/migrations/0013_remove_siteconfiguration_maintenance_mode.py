# Generated by Django 3.0.5 on 2020-04-05 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_siteconfiguration_keywords'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siteconfiguration',
            name='maintenance_mode',
        ),
    ]
