# Generated by Django 3.0.5 on 2020-04-04 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0017_auto_20200404_1710'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='thread',
            options={'permissions': [('lock_thread', 'Can lock a thread.'), ('locked_thread_reply', 'Can reply to a locked thread.')]},
        ),
    ]
