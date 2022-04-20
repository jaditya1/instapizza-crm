# Generated by Django 2.1.8 on 2020-02-25 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0026_auto_20200213_1852'),
        ('Brands', '0006_company_is_sound'),
        ('urbanpiper', '0016_actionsync'),
    ]

    operations = [
        migrations.CreateModel(
            name='CatSync',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_enabled', models.BooleanField(default=0, verbose_name='Is Synced')),
                ('is_available', models.BooleanField(default=0, verbose_name='Is Available')),
                ('urban_event', models.CharField(blank=True, choices=[('created', 'Category Created'), ('updated', 'Category Updated')], max_length=50, null=True, verbose_name='Event At UrbanPiper')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
                ('category', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='CatSync_category', to='Product.ProductCategory', verbose_name='Category')),
                ('company', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='CatSync_Company', to='Brands.Company', verbose_name='Company')),
                ('sync_outlet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CatSync_outlet', to='urbanpiper.OutletSync', verbose_name='Synced Outlet')),
            ],
            options={
                'verbose_name': '   Synced Category',
                'verbose_name_plural': '  Synced Categories',
            },
        ),
        migrations.CreateModel(
            name='ProductSync',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_enabled', models.BooleanField(default=0, verbose_name='Is Synced')),
                ('is_available', models.BooleanField(default=0, verbose_name='Is Available')),
                ('urban_event', models.CharField(blank=True, choices=[('created', 'Product Created'), ('updated', 'Product Updated')], max_length=50, null=True, verbose_name='Event At UrbanPiper')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
                ('category', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='ProductSync_category', to='Product.ProductCategory', verbose_name='Category')),
                ('company', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='ProductSync_Company', to='Brands.Company', verbose_name='Company')),
                ('product', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='ProductSync_product', to='Product.Product', verbose_name='Product')),
                ('sync_outlet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ProductSync_outlet', to='urbanpiper.OutletSync', verbose_name='Synced Outlet')),
            ],
            options={
                'verbose_name': '   Synced Product',
                'verbose_name_plural': '  Synced Products',
            },
        ),
    ]