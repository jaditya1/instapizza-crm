# Generated by Django 2.1.8 on 2020-02-13 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserRole', '0007_auto_20200212_2044'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainRoutingModule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module_id', models.CharField(max_length=100, unique=True, verbose_name='Module Id')),
                ('icon', models.CharField(max_length=100, verbose_name='Icon')),
                ('label', models.CharField(max_length=100, verbose_name='Label')),
                ('to', models.CharField(max_length=100, verbose_name='Url Path')),
                ('active_status', models.BooleanField(default=1, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
            ],
            options={
                'verbose_name': 'Main-Module Routing',
                'verbose_name_plural': '     Main-Module Routing',
            },
        ),
        migrations.CreateModel(
            name='RoutingModule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.CharField(max_length=100, verbose_name='Icon')),
                ('label', models.CharField(max_length=100, verbose_name='Label')),
                ('to', models.CharField(max_length=100, verbose_name='Url Path')),
                ('active_status', models.BooleanField(default=1, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
                ('main_route', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='RoutingModule_MainRoutingModule', to='UserRole.MainRoutingModule', verbose_name='Main Module')),
            ],
            options={
                'verbose_name': 'Module Routing',
                'verbose_name_plural': '    Module Routing',
            },
        ),
        migrations.CreateModel(
            name='SubRoutingModule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.CharField(max_length=100, verbose_name='Icon')),
                ('label', models.CharField(max_length=100, verbose_name='Label')),
                ('to', models.CharField(max_length=100, verbose_name='Url Path')),
                ('active_status', models.BooleanField(default=1, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
                ('route', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='SubRoutingModule_RoutingModule', to='UserRole.RoutingModule', verbose_name='Main Module')),
            ],
            options={
                'verbose_name': 'Sub-Module Routing',
                'verbose_name_plural': '   Sub-Module Routing',
            },
        ),
        migrations.AlterModelOptions(
            name='managerprofile',
            options={'verbose_name': 'Manager Profile', 'verbose_name_plural': '      Manager Profiles'},
        ),
        migrations.AlterModelOptions(
            name='usertype',
            options={'verbose_name': 'User Type', 'verbose_name_plural': '       User Type'},
        ),
    ]
