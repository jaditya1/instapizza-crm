# Generated by Django 2.1.8 on 2020-05-15 15:18

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0038_product_include_platform'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='include_platform',
        ),
        migrations.AddField(
            model_name='product',
            name='included_platform',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, null=True, size=None, verbose_name='Included Plateform'),
        ),
    ]
