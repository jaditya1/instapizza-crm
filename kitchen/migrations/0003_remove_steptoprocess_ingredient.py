# Generated by Django 2.1.8 on 2020-01-14 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0002_auto_20200114_1347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='steptoprocess',
            name='Ingredient',
        ),
    ]
