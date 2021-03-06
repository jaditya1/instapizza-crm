# Generated by Django 2.1.8 on 2019-11-23 08:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0004_coupon_is_automated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='flat_discount',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10000)], verbose_name='Flat Discount'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='flat_percentage',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10000)], verbose_name='Percentage Discount'),
        ),
    ]
