# Generated by Django 2.1.8 on 2019-11-28 07:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Outlet', '0002_auto_20191105_0003'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryBoy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='User Name')),
                ('email', models.EmailField(blank=True, max_length=100, null=True, unique=True, verbose_name='Email Id')),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='deliveryboy_profile', verbose_name='Profile Pic')),
                ('mobile', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Mobile')),
                ('address', models.CharField(max_length=150, verbose_name='Address')),
                ('active_status', models.BooleanField(default=1, verbose_name='Is Active')),
                ('is_assign', models.BooleanField(default=0, verbose_name='Is Assign')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
                ('Outlet', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='DeliveryBoy_OutletProfile', to='Outlet.OutletProfile', verbose_name='Outlet')),
            ],
            options={
                'verbose_name': 'DeliveryBoy',
                'verbose_name_plural': ' DeliveryBoy',
            },
        ),
    ]
