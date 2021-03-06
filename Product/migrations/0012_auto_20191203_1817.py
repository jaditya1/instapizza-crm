# Generated by Django 2.1.8 on 2019-12-03 12:47

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0011_product_availability'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='addpn_grp_association',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='product',
            name='outlet_map',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, size=None, verbose_name='Outlet Mapped Ids'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='outlet_map',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, size=None, verbose_name='Outlet Mapped Ids'),
        ),
    ]
