# Generated by Django 2.1.8 on 2019-11-03 13:54

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Configuration', '0002_remove_currencymaster_codeiso'),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.CharField(max_length=100, verbose_name='City Area')),
                ('active_status', models.BooleanField(default=1, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Creation Date')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date')),
            ],
            options={
                'verbose_name': 'Locality',
                'verbose_name_plural': 'Localities',
                'ordering': ['area'],
            },
        ),
        migrations.CreateModel(
            name='CityMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=35, verbose_name='City')),
                ('active_status', models.BooleanField(default=1, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Creation Date')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date')),
            ],
            options={
                'verbose_name': ' City',
                'verbose_name_plural': ' Cities',
                'ordering': ['city'],
            },
        ),
        migrations.CreateModel(
            name='CountryMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=35, unique=True, verbose_name='Country')),
                ('iso', models.CharField(max_length=4, verbose_name='ISO')),
                ('isd', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(999999), django.core.validators.MinValueValidator(1)], verbose_name='ISD/Country Code')),
                ('mobile_no_digits', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(15), django.core.validators.MinValueValidator(5)], verbose_name='Countries Mobile Number digit')),
                ('country_flag', models.ImageField(blank=True, null=True, upload_to='countryflag/', verbose_name='Country Flag')),
                ('active_status', models.BooleanField(default=1, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Creation Date')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date')),
                ('currency', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='country_master_currency', to='Configuration.CurrencyMaster', verbose_name='Currency')),
            ],
            options={
                'verbose_name': '   Country',
                'verbose_name_plural': '   Countries',
                'ordering': ['country'],
            },
        ),
        migrations.CreateModel(
            name='StateMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=35, verbose_name='State')),
                ('active_status', models.BooleanField(default=1, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Creation Date')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date')),
                ('country', models.ForeignKey(limit_choices_to={'active_status': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='state_master_state', to='Location.CountryMaster', verbose_name='Country')),
            ],
            options={
                'verbose_name': '  State',
                'verbose_name_plural': '  States',
                'ordering': ['state'],
            },
        ),
        migrations.AddField(
            model_name='citymaster',
            name='state',
            field=models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='city_master_city', to='Location.StateMaster', verbose_name='State'),
        ),
        migrations.AddField(
            model_name='areamaster',
            name='city',
            field=models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='city_area_city', to='Location.CityMaster', verbose_name='City'),
        ),
        migrations.AlterUniqueTogether(
            name='statemaster',
            unique_together={('country', 'state')},
        ),
        migrations.AlterUniqueTogether(
            name='citymaster',
            unique_together={('state', 'city')},
        ),
    ]
