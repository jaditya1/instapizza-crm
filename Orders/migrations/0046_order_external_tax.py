# Generated by Django 2.1.8 on 2020-07-22 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0045_order_is_logged'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='external_tax',
            field=models.FloatField(blank=True, max_length=99999.99, null=True, verbose_name='External Tax'),
        ),
    ]
