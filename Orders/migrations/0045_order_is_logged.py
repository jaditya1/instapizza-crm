# Generated by Django 2.1.8 on 2020-06-22 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0044_orderprocesstimelog'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_logged',
            field=models.BooleanField(default=0),
        ),
    ]
