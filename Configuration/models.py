from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField,JSONField
# from Brands.models import Company
# from Outlet.models import OutletProfile, DeliveryBoy


class BusinessType(models.Model):
	business_type = models.CharField(max_length=50, verbose_name='Business Type',
	                                           unique=True)
	description = models.CharField(max_length=200, null=True, blank=True, verbose_name=
		                                                        'Description')
	active_status = models.BooleanField(default=1, verbose_name='Is Active')
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																			'Updation Date & Time')

	class Meta:
		verbose_name = '    Brand Type'
		verbose_name_plural = '    Brand Types'
		ordering = ['business_type']


	def __str__(self):
		return self.business_type


class CurrencyMaster(models.Model):
	currency = models.CharField(max_length=30, unique=True,
	    error_messages={'unique':"Currency already exists with the given name."}, 
	                      verbose_name="Currency")
	symbol = models.CharField(max_length=20, verbose_name="Symbol")
	hexsymbol = models.CharField(max_length=7, verbose_name='Hex Symbol',
		                                                   blank=True, null=True)
	active_status = models.BooleanField(default=1, verbose_name='Is Active')
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																			'Updation Date & Time')

	class Meta:
		verbose_name = "   Currency"
		verbose_name_plural = "   Currencies"

	def __str__(self):
		return self.currency



class PaymentDetails(models.Model):
	name = models.CharField(max_length=50, null=True, blank=True, verbose_name="Payment Gateway Name")
	company = models.ForeignKey('Brands.Company', related_name='PaymentDetails_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	username = models.CharField(max_length=50, null=True, blank=True, verbose_name="User Name")
	keyid = models.CharField(max_length=50, null=True, blank=True, verbose_name="keyId")
	keySecret = models.CharField(max_length=50, null=True, blank=True, verbose_name="keySecret")
	symbol = models.CharField(max_length=50, null=True, blank=True, verbose_name="Currency")
	active_status = models.BooleanField(default=1, verbose_name='Is Active')
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																			'Updation Date & Time')

	class Meta:
		verbose_name = "   Payment Credential"
		verbose_name_plural = "   Payment Credential"

	def __str__(self):
		return str(self.company)


class ColorSetting(models.Model):
	accent_color = models.CharField(max_length=20, null=True, blank=True, 
				verbose_name="Accent color")
	textColor = models.CharField(max_length=20, null=True, blank=True, 
				verbose_name="Text color")
	secondaryColor = models.CharField(max_length=20, null=True, blank=True, 
				verbose_name="Secondary color")
	company = models.ForeignKey('Brands.Company', related_name='ColorSetting_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	active_status = models.BooleanField(default=1, verbose_name='Is Active')
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																			'Updation Date & Time')

	class Meta:
		verbose_name = "   Accent Color"
		verbose_name_plural = "   Color Setting"

	def __str__(self):
		return str(self.company) 


class DeliverySetting(models.Model):
	delivery_charge = models.FloatField(blank=True,null=True,verbose_name='Delivery Charge')
	package_charge = models.FloatField(blank=True,null=True,verbose_name='Package Charge')
	company = models.ForeignKey('Brands.Company', related_name='DeliverySetting_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	tax_percent = models.FloatField(verbose_name="SGST",null=True, blank=True)

	CGST = models.FloatField(verbose_name="CGST",null=True, blank=True)

	symbol = models.CharField(max_length=50, null=True, blank=True, verbose_name="Currency")
	active_status = models.BooleanField(default=1, verbose_name='Is Active')
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																			'Updation Date & Time')

	class Meta:
		verbose_name = "   Delivery Setting"
		verbose_name_plural = "   Delivery Settings"

	def __str__(self):
		return str(self.delivery_charge)


class AnalyticsSetting(models.Model):
	company = models.ForeignKey('Brands.Company', related_name='AnalyticsSetting_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	u_id = models.CharField(max_length=255,null=True, blank=True, verbose_name="Analytics U Id")
	analytics_snippets = \
	models.TextField(null=True, blank=True, verbose_name="Analytics Snippet")
	active_status = models.BooleanField(default=1, verbose_name='Is Active')
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																			'Updation Date & Time')

	class Meta:
		verbose_name = "   Google Analytics Setting"
		verbose_name_plural = "   Google Analytics Settings"

	def __str__(self):
		return str(self.u_id)


class EmailSetting(models.Model):
	company = models.ForeignKey('Brands.Company', related_name='EmailSetting_Company',
										on_delete=models.CASCADE,verbose_name='Company',
										limit_choices_to={'active_status':'1'})
	title = models.CharField(max_length=255,null=True, blank=True, verbose_name="Title")
	image = models.ImageField(upload_to='EmailSetting',null=True, blank=True, verbose_name='image')
	content = models.CharField(max_length=255,null=True, blank=True, verbose_name="Content")
	thank = models.CharField(max_length=255,null=True, blank=True, verbose_name="thank")
	dis_content = models.CharField(max_length=255,null=True, blank=True, verbose_name="Discount Content")
	coupon = models.ForeignKey('discount.PercentOffers',null=True,blank=True, related_name='EmailSetting_coupon',
										on_delete=models.CASCADE,verbose_name='Coupon',
										limit_choices_to={'active_status':'1'})
	active_status = models.BooleanField(default=1, verbose_name='Is Active')
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																			'Updation Date & Time')

	class Meta:
		verbose_name = " Email Setting"
		verbose_name_plural = " Email Settings"

	def __str__(self):
		return str(self.company)


class Excelimport(models.Model):
	title = models.CharField(max_length=255,null=True, blank=True, verbose_name="Title")
	image = models.ImageField(upload_to='import',null=True, blank=True, verbose_name='image')
	active_status = models.BooleanField(default=1, verbose_name='Is Active')
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																			'Updation Date & Time')

	class Meta:
		verbose_name = "   Excel Import"
		verbose_name_plural = "   Excel Import"

	def __str__(self):
		return str(self.title)




class TaxSetting(models.Model):
	company = models.ForeignKey('Brands.Company', related_name='TaxSetting_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	tax_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="Tax Name")
	tax_percent = models.FloatField(verbose_name="Percentage",null=True, blank=True)
	active_status = models.BooleanField(default=1, verbose_name='Is Active')
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																			'Updation Date & Time')

	class Meta:
		verbose_name = "   Tax Setting"
		verbose_name_plural = "   Tax Settings"

	def __str__(self):
		return str(self.tax_name)


class HeaderFooter(models.Model):
	outlet = models.ForeignKey('Outlet.OutletProfile',on_delete=models.CASCADE,verbose_name='Outlet',
												limit_choices_to={'active_status':'1'},
												blank=True, null=True)
	company = models.ForeignKey('Brands.Company', related_name='HeaderFooter_Company',
										on_delete=models.CASCADE,verbose_name='Company',
										limit_choices_to={'active_status':'1'})
	header_text = models.TextField(null=True, blank=True, verbose_name="Header Text")
	footer_text = models.TextField(verbose_name="Footer Text",null=True, blank=True)
	gst = models.CharField(max_length=50, null=True, blank=True, verbose_name="GST")
	active_status = models.BooleanField(default=1, verbose_name='Is Active')
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = "   Receipt Configuration"
		verbose_name_plural = "   Receipt Configuration"

	def __str__(self):
		return str(self.gst)


class DailyMailReporter(models.Model):
	email = \
	models.CharField(max_length=255,null=True, blank=True, verbose_name="Email")
	mail_response = \
	JSONField(blank=True,null=True, verbose_name="Mail SEnding Response")
	mail_type = \
	models.CharField(max_length=255,null=True, blank=True, verbose_name="Email Type")
	is_success = models.BooleanField(default=0, verbose_name='Is Delivered')
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')


	class Meta:
		verbose_name = "   Daliy Mail Reporter"
		verbose_name_plural = "   Daliy Mail Reporter"

	def __str__(self):
		return str(self.email)