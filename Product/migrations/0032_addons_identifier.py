# Generated by Django 2.1.8 on 2020-03-27 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0031_addondetails_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='addons',
            name='identifier',
            field=models.CharField(default=1, max_length=250, verbose_name='Add on Identifier'),
            preserve_default=False,
        ),
    ]
