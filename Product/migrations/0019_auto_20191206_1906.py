# Generated by Django 2.1.8 on 2019-12-06 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0018_auto_20191206_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Company',
            field=models.ForeignKey(blank=True, limit_choices_to={'active_status': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Product_Company', to='Brands.Company', verbose_name='Company'),
        ),
    ]
