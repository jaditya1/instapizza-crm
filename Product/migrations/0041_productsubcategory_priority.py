# Generated by Django 2.1.8 on 2020-09-21 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0040_addondetails_is_crust'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsubcategory',
            name='priority',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Priority'),
        ),
    ]
