# Generated by Django 2.1.8 on 2020-05-24 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0040_auto_20200523_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='special_instructions',
            field=models.TextField(blank=True, null=True, verbose_name='Special Instructions'),
        ),
    ]
