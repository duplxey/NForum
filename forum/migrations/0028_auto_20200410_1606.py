# Generated by Django 3.0.5 on 2020-04-10 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0027_auto_20200407_1816'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='thread',
            options={'ordering': ['-pk'], 'permissions': [('locked_thread_reply', 'Can reply to a locked thread.'), ('create_thread_in_staff_only', 'Can create threads in staff only categories.')]},
        ),
    ]