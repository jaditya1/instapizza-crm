# Generated by Django 2.1.8 on 2020-02-05 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Configuration', '0010_auto_20200205_1236'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverysetting',
            name='CGST',
            field=models.FloatField(blank=True, null=True, verbose_name='CGST'),
        ),
        migrations.AlterField(
            model_name='deliverysetting',
            name='tax_percent',
            field=models.FloatField(blank=True, null=True, verbose_name='SGST'),
        ),
    ]
