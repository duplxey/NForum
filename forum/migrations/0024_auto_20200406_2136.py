# Generated by Django 3.0.5 on 2020-04-06 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0023_auto_20200406_2136'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subcategory',
            options={'ordering': ['-y_display'], 'verbose_name_plural': 'subcategories'},
        ),
        migrations.AddField(
            model_name='subcategory',
            name='y_display',
            field=models.SmallIntegerField(default=-1),
        ),
    ]
