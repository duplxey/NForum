# Generated by Django 2.2.5 on 2019-10-16 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0006_auto_20191016_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wikipage',
            name='url',
            field=models.CharField(max_length=64),
        ),
    ]
