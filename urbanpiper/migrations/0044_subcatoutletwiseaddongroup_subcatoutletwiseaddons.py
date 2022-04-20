# Generated by Django 2.1.8 on 2020-10-18 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0041_productsubcategory_priority'),
        ('Outlet', '0027_outletprofile_gst'),
        ('urbanpiper', '0043_zomatomenutemporaryitemdata_is_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubCatOutletWiseAddonGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_available', models.BooleanField(default=1, verbose_name='Is Accepted')),
                ('active_status', models.BooleanField(default=1, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
                ('addon_group', models.ForeignKey(blank=True, limit_choices_to={'active_status': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='addon_grouping', to='Product.AddonDetails', verbose_name='Add-On Group')),
                ('outlet', models.ForeignKey(blank=True, limit_choices_to={'active_status': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='AddonGroup_OutletProfile', to='Outlet.OutletProfile', verbose_name='Outlet')),
            ],
            options={
                'verbose_name': 'Synced Outlet Wise Addon Groups',
                'verbose_name_plural': 'Synced Outlet Wise Addon Groups',
            },
        ),
        migrations.CreateModel(
            name='SubCatOutletWiseAddons',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_available', models.BooleanField(default=1, verbose_name='Is Accepted')),
                ('active_status', models.BooleanField(default=1, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
                ('addon_id', models.ForeignKey(blank=True, limit_choices_to={'active_status': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='addon_id', to='Product.Addons', verbose_name='Add-On Group')),
                ('outlet', models.ForeignKey(blank=True, limit_choices_to={'active_status': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Addon_OutletProfile', to='Outlet.OutletProfile', verbose_name='Outlet')),
            ],
            options={
                'verbose_name': 'Synced Outlet Wise Addons',
                'verbose_name_plural': 'Synced Outlet Wise Addons',
            },
        ),
    ]
