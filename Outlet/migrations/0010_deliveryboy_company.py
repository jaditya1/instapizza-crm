# Generated by Django 2.1.8 on 2020-03-19 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Brands', '0007_company_is_open'),
        ('Outlet', '0009_auto_20200319_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryboy',
            name='Company',
            field=models.ForeignKey(blank=True, limit_choices_to={'active_status': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='DeliveryBoy_Company', to='Brands.Company', verbose_name='Company'),
        ),
    ]
