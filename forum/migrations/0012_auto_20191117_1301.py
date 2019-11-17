# Generated by Django 2.2.5 on 2019-11-17 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0011_auto_20191116_0012'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='threadprefix',
            options={'verbose_name_plural': 'thread prefixes'},
        ),
        migrations.AlterField(
            model_name='thread',
            name='prefix',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='forum.ThreadPrefix'),
        ),
    ]
