# Generated by Django 2.1.8 on 2020-03-27 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urbanpiper', '0024_auto_20200325_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsync',
            name='product_status',
            field=models.CharField(choices=[('enabled', 'Enabled'), ('disabled', 'Disabled'), ('in_progress', 'In Progress')], default='enabled', max_length=50, verbose_name='Sync Status'),
        ),
    ]
