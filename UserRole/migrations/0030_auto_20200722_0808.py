# Generated by Django 2.1.8 on 2020-07-22 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserRole', '0029_managerprofile_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='managerprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True, verbose_name='Email Id'),
        ),
    ]