# Generated by Django 2.1.8 on 2020-07-25 03:30

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Configuration', '0015_headerfooter'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyMailReporter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(blank=True, max_length=255, null=True, verbose_name='Email')),
                ('mail_response', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='Mail SEnding Response')),
                ('mail_type', models.CharField(blank=True, max_length=255, null=True, verbose_name='Email Type')),
                ('is_success', models.BooleanField(default=0, verbose_name='Is Delivered')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
            ],
            options={
                'verbose_name': '   Daliy Mail Reporter',
                'verbose_name_plural': '   Daliy Mail Reporter',
            },
        ),
    ]
