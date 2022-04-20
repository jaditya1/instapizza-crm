# Generated by Django 2.1.8 on 2020-05-22 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Brands', '0007_company_is_open'),
        ('Outlet', '0015_outletprofile_cam_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='outletprofile',
            name='priority',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Priority'),
        ),
        migrations.AlterField(
            model_name='deliveryboy',
            name='mobile',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Mobile'),
        ),
        migrations.AlterUniqueTogether(
            name='outletprofile',
            unique_together={('Company', 'priority')},
        ),
    ]
