# Generated by Django 2.1.8 on 2020-02-19 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urbanpiper', '0007_auto_20200219_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='outletsync',
            name='urbanpiper_store_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='UrbanPiper Store Id'),
        ),
    ]
