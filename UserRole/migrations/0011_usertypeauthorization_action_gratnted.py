# Generated by Django 2.1.8 on 2020-02-14 08:03

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserRole', '0010_usertypeauthorization'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertypeauthorization',
            name='action_gratnted',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]