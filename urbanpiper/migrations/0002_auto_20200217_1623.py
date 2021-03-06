# Generated by Django 2.1.8 on 2020-02-17 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Outlet', '0007_outletprofile_user_type'),
        ('Brands', '0006_company_is_sound'),
        ('urbanpiper', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OutletSync',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_synced', models.BooleanField(default=0, verbose_name='Is Synced')),
                ('sync_status', models.CharField(choices=[('not_intiated', 'Not Initiated'), ('in_progress', 'In Progress'), ('synced', 'Synced')], max_length=50, verbose_name='Sync Status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
                ('company', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='OutletSync_Company', to='Brands.Company', verbose_name='Company')),
                ('outlet', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='OutletSync_outlet', to='Outlet.OutletProfile', verbose_name='Outlet')),
            ],
            options={
                'verbose_name': '   Outlet Sync Status',
                'verbose_name_plural': '   Outlet Sync Status',
            },
        ),
        migrations.AlterModelOptions(
            name='eventtypes',
            options={'verbose_name': '    Event Type', 'verbose_name_plural': '    Event Types'},
        ),
        migrations.AlterModelOptions(
            name='urbancred',
            options={'verbose_name': '    Account Credential', 'verbose_name_plural': '    Account Credential'},
        ),
        migrations.AlterModelOptions(
            name='webhooks',
            options={'verbose_name': '    WebHook Setting', 'verbose_name_plural': '    WebHook Setting'},
        ),
        migrations.RemoveField(
            model_name='apireference',
            name='is_synced',
        ),
        migrations.AddField(
            model_name='outletsync',
            name='ref_id',
            field=models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='OutletSync_ref', to='urbanpiper.APIReference', verbose_name='API Reference Id'),
        ),
    ]
