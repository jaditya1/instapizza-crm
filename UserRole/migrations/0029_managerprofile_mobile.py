# Generated by Django 2.1.8 on 2020-07-12 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserRole', '0028_auto_20200524_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='managerprofile',
            name='mobile',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Mobile'),
        ),
    ]
