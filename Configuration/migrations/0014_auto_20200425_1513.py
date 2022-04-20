# Generated by Django 2.1.8 on 2020-04-25 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Brands', '0007_company_is_open'),
        ('Configuration', '0013_excelimport'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaxSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tax_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Tax Name')),
                ('tax_percent', models.FloatField(blank=True, null=True, verbose_name='Percentage')),
                ('active_status', models.BooleanField(default=1, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
                ('company', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='TaxSetting_Company', to='Brands.Company', verbose_name='Company')),
            ],
            options={
                'verbose_name': '   Tax Setting',
                'verbose_name_plural': '   Tax Settings',
            },
        ),
        migrations.AlterModelOptions(
            name='deliverysetting',
            options={'verbose_name': '   Delivery Setting', 'verbose_name_plural': '   Delivery Settings'},
        ),
    ]
