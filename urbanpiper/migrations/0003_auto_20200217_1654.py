# Generated by Django 2.1.8 on 2020-02-17 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Brands', '0006_company_is_sound'),
        ('urbanpiper', '0002_auto_20200217_1623'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='eventtypes',
            unique_together={('company', 'event_type')},
        ),
    ]
