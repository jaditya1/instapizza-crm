# Generated by Django 2.1.8 on 2020-08-31 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urbanpiper', '0042_auto_20200831_0805'),
    ]

    operations = [
        migrations.AddField(
            model_name='zomatomenutemporaryitemdata',
            name='is_size',
            field=models.BooleanField(default=0, verbose_name='Is Size'),
        ),
    ]
