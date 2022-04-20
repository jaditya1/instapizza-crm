# Generated by Django 2.1.8 on 2020-02-03 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Configuration', '0007_deliverysetting'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deliverysetting',
            options={'verbose_name': '   Delivery & Tax Setting', 'verbose_name_plural': '   Delivery & Tax Settings'},
        ),
        migrations.AddField(
            model_name='deliverysetting',
            name='tax_percent',
            field=models.FloatField(blank=True, null=True, verbose_name='Tax Percentage'),
        ),
        migrations.AlterField(
            model_name='deliverysetting',
            name='symbol',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Currency'),
        ),
        migrations.AlterField(
            model_name='paymentdetails',
            name='symbol',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Currency'),
        ),
    ]