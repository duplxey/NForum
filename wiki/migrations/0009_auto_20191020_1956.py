# Generated by Django 2.2.5 on 2019-10-20 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0008_auto_20191020_1200'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wikipage',
            options={'ordering': ['display_index']},
        ),
        migrations.AlterField(
            model_name='wikipage',
            name='url',
            field=models.SlugField(max_length=64, unique=True),
        ),
    ]
