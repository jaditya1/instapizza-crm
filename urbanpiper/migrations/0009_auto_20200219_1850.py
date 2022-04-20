# Generated by Django 2.1.8 on 2020-02-19 13:20

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('urbanpiper', '0008_outletsync_urbanpiper_store_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='apireference',
            name='api_response',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='apireference',
            name='error_api_response',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='apireference',
            name='event_type',
            field=models.ForeignKey(default=1, limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='APIReference_event_type', to='urbanpiper.EventTypes', verbose_name='Event Type'),
            preserve_default=False,
        ),
    ]
