# Generated by Django 2.1.8 on 2019-11-23 08:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0005_auto_20191123_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='frequency',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10000)], verbose_name='Priority'),
        ),
    ]
