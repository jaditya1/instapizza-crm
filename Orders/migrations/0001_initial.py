# Generated by Django 2.1.8 on 2019-11-24 07:37

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Brands', '0004_auto_20191120_1650'),
        ('Outlet', '0002_auto_20191105_0003'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, max_length=150, null=True, verbose_name='Order Id')),
                ('address', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='Address Details')),
                ('customer', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='Customer Details')),
                ('Company_outlet_details', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='Company & Outlet Details')),
                ('order_description', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='Order Description')),
                ('order_time', models.DateTimeField(blank=True, null=True, verbose_name='Order Time')),
                ('delivery_time', models.DateTimeField(blank=True, null=True, verbose_name='Delivery Time')),
                ('taxes', models.FloatField(blank=True, max_length=99999.99, null=True, verbose_name='Tax')),
                ('payment_mode', models.CharField(blank=True, choices=[('0', 'Cash on Delivery'), ('1', 'Online')], max_length=150, null=True, verbose_name='Payment Mode')),
                ('special_instructions', models.CharField(blank=True, max_length=255, null=True, verbose_name='Special Instructions')),
                ('sub_total', models.FloatField(blank=True, null=True, verbose_name='Sub Total')),
                ('discount_value', models.FloatField(blank=True, null=True, verbose_name='Discount Value')),
                ('payment_id', models.CharField(blank=True, max_length=150, null=True, verbose_name='Payment Id')),
                ('coupon_code', models.CharField(blank=True, max_length=150, null=True, verbose_name='Coupon Code')),
                ('is_paid', models.BooleanField(blank=True, null=True, verbose_name='Is Paid')),
                ('total_bill_value', models.FloatField(blank=True, null=True, verbose_name='Total Bill Value')),
                ('total_items', models.PositiveIntegerField(blank=True, null=True, verbose_name='Total Items')),
                ('Company', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='Order_Company', to='Brands.Company', verbose_name='Company')),
            ],
            options={
                'verbose_name': 'Order Management',
                'verbose_name_plural': ' Order Management',
            },
        ),
        migrations.CreateModel(
            name='OrderStatusType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Order_staus_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Order Status Name')),
                ('active_status', models.BooleanField(default=1, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
            ],
            options={
                'verbose_name': 'Order Status Type',
                'verbose_name_plural': '  Order Status Type',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.ForeignKey(blank=True, limit_choices_to={'active_status': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Order_OrderStatusType', to='Orders.OrderStatusType', verbose_name='Order Status'),
        ),
        migrations.AddField(
            model_name='order',
            name='outlet',
            field=models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='Order_OutletProfile', to='Outlet.OutletProfile', verbose_name='Outlet'),
        ),
    ]
