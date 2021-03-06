# Generated by Django 2.1.8 on 2020-02-29 04:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0030_addons_updated_at'),
        ('urbanpiper', '0018_auto_20200226_1917'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsync',
            name='variant',
            field=models.ForeignKey(blank=True, limit_choices_to={'active_status': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ProductSync_Variant', to='Product.Variant', verbose_name='Variant'),
        ),
    ]
