# Generated by Django 2.1.8 on 2020-02-13 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0025_auto_20200210_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='food_type',
            field=models.ForeignKey(blank=True, limit_choices_to={'active_status': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Tag_food', to='Product.FoodType', verbose_name='Food Type'),
        ),
    ]
