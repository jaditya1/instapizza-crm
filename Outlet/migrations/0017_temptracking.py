# Generated by Django 2.1.8 on 2020-05-24 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Brands', '0007_company_is_open'),
        ('UserRole', '0028_auto_20200524_1537'),
        ('Outlet', '0016_auto_20200522_0932'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempTracking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body_temp', models.FloatField(verbose_name='Body Temp in F')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Date & Time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Date & Time')),
                ('Company', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='TempTracking_Company', to='Brands.Company', verbose_name='Company')),
                ('staff', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='TempTracking_staff', to='UserRole.ManagerProfile', verbose_name='Staff Mmeber')),
            ],
            options={
                'verbose_name': 'Staff Temperature Tracking',
                'verbose_name_plural': '   Staff Temperature Tracking',
            },
        ),
    ]
