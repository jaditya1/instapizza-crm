# Generated by Django 2.1.8 on 2020-08-12 06:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('UserRole', '0030_auto_20200722_0808'),
    ]

    operations = [
        migrations.CreateModel(
            name='DownloadToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auth_token', models.CharField(max_length=255, verbose_name='Authentication Token')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date')),
                ('auth_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='DownloadToken_auth_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Authentication Manager',
                'verbose_name_plural': 'Authentication Manager',
            },
        ),
    ]
