# Generated by Django 2.1.8 on 2019-12-03 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0007_orderstatustype_color_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderstatustype',
            name='is_delivery_boy',
            field=models.CharField(blank=True, choices=[('1', 'Yes'), ('0', 'No')], max_length=100, null=True, verbose_name='Can Assign to Delivery Boy'),
        ),
        migrations.AddField(
            model_name='orderstatustype',
            name='priority',
            field=models.PositiveIntegerField(blank=True, null=True, unique=True, verbose_name='Priority'),
        ),
    ]
