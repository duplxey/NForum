# Generated by Django 3.0.5 on 2020-04-06 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0020_auto_20200406_2029'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['display_index'], 'verbose_name_plural': 'categories'},
        ),
        migrations.AddField(
            model_name='category',
            name='display_index',
            field=models.SmallIntegerField(default=0),
        ),
    ]