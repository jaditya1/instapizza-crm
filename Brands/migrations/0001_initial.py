# Generated by Django 2.1.8 on 2019-11-03 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Location', '0001_initial'),
        ('Configuration', '0002_remove_currencymaster_codeiso'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=50, verbose_name='Brand Name')),
                ('username', models.CharField(max_length=100, unique=True, verbose_name='User Name')),
                ('password', models.CharField(max_length=20, verbose_name='Password')),
                ('address', models.CharField(max_length=250, verbose_name='Address')),
                ('zipcode', models.CharField(max_length=6, verbose_name='PIN Code')),
                ('company_logo', models.ImageField(blank=True, null=True, upload_to='company_logo', verbose_name='Company Logo')),
                ('company_registrationNo', models.CharField(max_length=25, verbose_name='Company Registration No.')),
                ('company_tinnNo', models.CharField(blank=True, max_length=11, null=True, verbose_name='TIN No.')),
                ('company_vatNo', models.CharField(blank=True, max_length=13, null=True, verbose_name='VAT No.')),
                ('company_gstNo', models.CharField(blank=True, max_length=15, null=True, verbose_name='GST No.')),
                ('website', models.URLField(blank=True, max_length=50, null=True, verbose_name='Company Website')),
                ('company_contact_no', models.CharField(max_length=15, verbose_name='Contact No.')),
                ('company_email_id', models.EmailField(max_length=50, verbose_name='Contact Email Id')),
                ('support_person', models.CharField(max_length=50, verbose_name='Support Person Name')),
                ('support_person_mobileno', models.CharField(help_text='Please enter Country /ISD code before mobile number', max_length=15, verbose_name='Support Mobile No.')),
                ('support_person_email_id', models.EmailField(max_length=255, verbose_name='Support Email ID')),
                ('support_person_landlineno', models.CharField(max_length=15, verbose_name='Support Landline No.')),
                ('contact_person', models.CharField(max_length=50, verbose_name='Contact Person Name')),
                ('contact_person_mobileno', models.CharField(help_text='Please enter Country /ISD code before mobile number', max_length=15, verbose_name='Contact Mobile No.')),
                ('contact_person_email_id', models.EmailField(max_length=255, verbose_name='Contact Other Email ID')),
                ('contact_person_landlineno', models.CharField(max_length=15, verbose_name='Contact Landline No.')),
                ('owner_name', models.CharField(max_length=50, verbose_name='Owner Name')),
                ('owner_email', models.EmailField(max_length=255, verbose_name='Owner Email Id')),
                ('owner_phone', models.CharField(help_text='Please enter Country /ISD code before mobile number', max_length=15, verbose_name='Owner Mobile No.')),
                ('billing_address', models.CharField(blank=True, max_length=250, null=True, verbose_name='Billing Address')),
                ('active_status', models.BooleanField(default=1, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Creation Date')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date')),
                ('billing_city', models.ForeignKey(blank=True, limit_choices_to={'active_status': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_billing_city', to='Location.CityMaster', verbose_name='Billing City')),
                ('billing_country', models.ForeignKey(blank=True, limit_choices_to={'active_status': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_billing_country', to='Location.CountryMaster', verbose_name='Billing Country')),
                ('billing_currency', models.ForeignKey(blank=True, limit_choices_to={'active_status': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_billing_currency', to='Configuration.CurrencyMaster', verbose_name='Billing Currency')),
                ('billing_state', models.ForeignKey(blank=True, limit_choices_to={'active_status': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_billing_state', to='Location.StateMaster', verbose_name='Billing State')),
                ('business_nature', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, to='Configuration.BusinessType', verbose_name='Business Nature')),
                ('city', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='company_city', to='Location.CityMaster', verbose_name='City')),
                ('country', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='company_country', to='Location.CountryMaster', verbose_name='Country')),
                ('state', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='company_state', to='Location.StateMaster', verbose_name='State')),
            ],
            options={
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brands',
            },
        ),
    ]
