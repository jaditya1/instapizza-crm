# Generated by Django 2.1.8 on 2020-05-09 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0037_product_is_recommended'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='include_platform',
            field=models.CharField(choices=[('1', 'Swiggy'), ('2', 'Zomato')], default='1', max_length=1),
        ),
    ]