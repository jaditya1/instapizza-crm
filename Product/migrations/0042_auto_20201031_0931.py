# Generated by Django 2.1.8 on 2020-10-31 04:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Brands', '0008_auto_20200812_1141'),
        ('Product', '0041_productsubcategory_priority'),
    ]

    operations = [
        migrations.CreateModel(
            name='KotSteps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kot_category', models.CharField(blank=True, choices=[(0, 'Make Line'), (1, 'Cut Table')], max_length=50, null=True, verbose_name='KOT Catefory Type')),
                ('step_name', models.CharField(blank=True, choices=[(0, 'Description'), (1, 'Crust'), (2, 'Base Sauce'), (3, 'Cut Table'), (4, 'Toppings'), (5, 'Additional Toppings'), (6, 'Cheese'), (7, 'Extra Cheese'), (8, 'Sauce on Top'), (9, 'Garnishes'), (10, 'Add-ons')], max_length=50, null=True, verbose_name='Step Name')),
                ('kot_desc', models.TextField(blank=True, null=True, verbose_name='KOT Description')),
                ('active_status', models.BooleanField(default=1, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
                ('Company', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='KotSteps_Company', to='Brands.Company', verbose_name='Company')),
                ('product', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='KotSteps_Product', to='Product.Product', verbose_name='Product')),
            ],
            options={
                'verbose_name': ' Item KOT Description',
                'verbose_name_plural': ' Item KOT Description',
            },
        ),
        migrations.AddField(
            model_name='addondetails',
            name='sync_status',
            field=models.CharField(blank=True, choices=[(0, 'Is Crust'), (1, 'Is Sauce'), (2, 'Is Cheese'), (3, 'Is Topping')], max_length=50, null=True, verbose_name='Addon Group Type'),
        ),
    ]
