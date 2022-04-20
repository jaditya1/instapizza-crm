# Generated by Django 2.1.8 on 2019-11-22 14:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0002_auto_20191122_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='flat_discount',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10000)], verbose_name='Flat Discount'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='flat_percentage',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10000)], verbose_name='Percentage Discount'),
        ),
    ]