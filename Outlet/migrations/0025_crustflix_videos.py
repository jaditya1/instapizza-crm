# Generated by Django 2.1.8 on 2020-09-21 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Outlet', '0024_auto_20200812_1141'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crustflix_Videos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('youtube_url', models.URLField(max_length=300, verbose_name='Youtube URL')),
                ('active_status', models.BooleanField(default=0, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Date & Time')),
            ],
            options={
                'verbose_name': 'Crustflix Videos',
                'verbose_name_plural': ' Crustflix Videos',
            },
        ),
    ]
