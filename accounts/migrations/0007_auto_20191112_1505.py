# Generated by Django 2.2.5 on 2019-11-12 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20191112_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='message',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
    ]