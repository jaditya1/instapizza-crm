# Generated by Django 2.1.8 on 2020-03-27 03:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserRole', '0017_managerprofile_outlet'),
    ]

    operations = [
        migrations.CreateModel(
            name='RollPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('per_label', models.CharField(blank=True, max_length=100, null=True, verbose_name='Permission Field')),
                ('active_status', models.BooleanField(default=1, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
                ('main_route', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='RollPermission_main_route', to='UserRole.MainRoutingModule', verbose_name='Main Module')),
                ('route', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='RollPermission_route', to='UserRole.RoutingModule', verbose_name='Module')),
                ('sub_route', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='RollPermission_sub_route', to='UserRole.SubRoutingModule', verbose_name='Module')),
                ('user_type', models.ForeignKey(blank=True, limit_choices_to={'active_status': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='RollPermission_UserType', to='UserRole.UserType', verbose_name='User Type')),
            ],
            options={
                'verbose_name': 'RollPermission',
                'verbose_name_plural': '    RollPermission',
            },
        ),
    ]
