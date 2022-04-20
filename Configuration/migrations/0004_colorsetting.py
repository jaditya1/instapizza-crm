# Generated by Django 2.1.8 on 2020-01-17 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Brands', '0006_company_is_sound'),
        ('Configuration', '0003_paymentdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColorSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accent_color', models.CharField(blank=True, max_length=20, null=True, verbose_name='Accent color')),
                ('active_status', models.BooleanField(default=1, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
                ('company', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='ColorSetting_Company', to='Brands.Company', verbose_name='Company')),
            ],
            options={
                'verbose_name': '   Accent Color',
                'verbose_name_plural': '   Color Setting',
            },
        ),
    ]