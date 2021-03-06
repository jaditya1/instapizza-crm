# Generated by Django 2.1.8 on 2020-03-05 04:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0015_auto_20200305_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='outlet',
            field=models.ForeignKey(blank=True, limit_choices_to={'active_status': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Order_OutletProfile', to='Outlet.OutletProfile', verbose_name='Outlet'),
        ),
    ]
