# Generated by Django 2.1.8 on 2020-02-17 04:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Brands', '0006_company_is_sound'),
        ('pos', '0002_posorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='posorder',
            name='company',
            field=models.ForeignKey(blank=True, limit_choices_to={'active_status': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='POSOrder_Company', to='Brands.Company', verbose_name='Company'),
        ),
        migrations.AddField(
            model_name='posorder',
            name='diff_amount',
            field=models.FloatField(blank=True, null=True, verbose_name='Difference Amount'),
        ),
    ]