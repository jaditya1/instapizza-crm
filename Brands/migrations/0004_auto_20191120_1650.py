# Generated by Django 2.1.8 on 2019-11-20 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Brands', '0003_auto_20191103_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='support_person',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Support Person Name'),
        ),
    ]
