# Generated by Django 2.1.8 on 2020-01-22 05:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0021_product_discount_price'),
        ('kitchen', '0009_auto_20200121_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='processtrack',
            name='Variant',
            field=models.ForeignKey(blank=True, limit_choices_to={'active_status': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ProcessTrack_Variant', to='Product.Variant', verbose_name='Variant'),
        ),
        migrations.AlterField(
            model_name='processtrack',
            name='Order',
            field=models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='ProcessTrack_Order', to='Orders.Order', verbose_name='Order'),
        ),
    ]
