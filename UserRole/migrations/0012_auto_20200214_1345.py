# Generated by Django 2.1.8 on 2020-02-14 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserRole', '0011_usertypeauthorization_action_gratnted'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usertypeauthorization',
            old_name='action_gratnted',
            new_name='action_granted',
        ),
    ]
