# Generated by Django 2.2.5 on 2019-10-09 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_message_thread'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
