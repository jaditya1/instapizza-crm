# Generated by Django 2.1.8 on 2020-03-05 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0030_addons_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='addondetails',
            name='description',
            field=models.CharField(blank=True, max_length=200, verbose_name='Description'),
        ),
    ]