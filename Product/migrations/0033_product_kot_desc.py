# Generated by Django 2.1.8 on 2020-04-03 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0032_addons_identifier'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='kot_desc',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Kot Description'),
        ),
    ]
