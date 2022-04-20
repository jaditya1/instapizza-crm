# Generated by Django 2.1.8 on 2020-01-28 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Configuration', '0005_auto_20200122_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentdetails',
            name='keySecret',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='keySecret'),
        ),
        migrations.AlterField(
            model_name='paymentdetails',
            name='keyid',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='keyId'),
        ),
        migrations.AlterField(
            model_name='paymentdetails',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Payment Gateway Name'),
        ),
        migrations.AlterField(
            model_name='paymentdetails',
            name='symbol',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Currency Symbol'),
        ),
        migrations.AlterField(
            model_name='paymentdetails',
            name='username',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='User Name'),
        ),
    ]