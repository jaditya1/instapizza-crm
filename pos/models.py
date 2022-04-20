from django.db import models
from Brands.models import Company
# Create your models here.
class POSOrder(models.Model):
	created_on = models.DateTimeField(null=True, blank=True, verbose_name='Created On')
	customer_name = models.CharField(max_length=150,null=True, blank=True, verbose_name='Customet Name')
	customer_number = models.CharField(max_length=150,blank=True,null=True,verbose_name='customer_number')
	date = models.DateTimeField(null=True, blank=True, verbose_name='Date')
	discount_value = models.FloatField(blank=True,null=True,verbose_name='Discount Value')
	external_id = models.CharField(max_length=150,null=True, blank=True, verbose_name='External ID')


	ids = models.CharField(max_length=150,null=True, blank=True, verbose_name='IDs')
	invoice_number = models.CharField(max_length=150,null=True, blank=True, verbose_name='Invoice Number')
	order_type = models.CharField(max_length=150,blank=True,null=True,verbose_name='Order Type')
	outlet = models.CharField(max_length=150,null=True, blank=True, verbose_name='Outlet')
	payment_mode = models.CharField(max_length=150,blank=True,null=True,verbose_name='Payment Mode')
	rider_name = models.CharField(max_length=150,null=True, blank=True, verbose_name='Rider Name')
	rider_number = models.CharField(max_length=150,null=True, blank=True, verbose_name='Rider Number')
	source = models.CharField(max_length=150,null=True, blank=True, verbose_name='Source')
	status_name = models.CharField(max_length=150,null=True, blank=True, verbose_name='Status Name')
	sub_total = models.FloatField(null=True, blank=True, verbose_name='Sub Total')
	time = models.TimeField(auto_now=False, auto_now_add=False, null=True,blank=True,
											verbose_name="Time")
	total = models.FloatField(blank=True,null=True,verbose_name='Total')
	subtotal = models.FloatField(blank=True,null=True,verbose_name='Sub Total')
	total_tax = models.FloatField(blank=True,null=True,verbose_name='Total Tax')
	diff_amount = models.FloatField(blank=True,null=True,verbose_name='Difference Amount')
	user_name = models.CharField(max_length=150,null=True, blank=True, verbose_name='User Name')
	company = models.ForeignKey(Company,blank=True,null=True, related_name='POSOrder_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})



	class Meta:
		verbose_name = 'POS Management'
		verbose_name_plural = ' POS Management'

	def __str__(self):
		return self.source


class SushiyaCustomer(models.Model):
	created_on = models.DateTimeField(null=True, blank=True, verbose_name='Created On')
	customer_name = models.CharField(max_length=150,null=True, blank=True, verbose_name='Customet Name')
	customer_number = models.CharField(max_length=150,blank=True,null=True,verbose_name='customer_number')
	date = models.DateTimeField(null=True, blank=True, verbose_name='Date')
	discount_value = models.FloatField(blank=True,null=True,verbose_name='Discount Value')
	external_id = models.CharField(max_length=150,null=True, blank=True, verbose_name='External ID')


	ids = models.CharField(max_length=150,null=True, blank=True, verbose_name='IDs')
	invoice_number = models.CharField(max_length=150,null=True, blank=True, verbose_name='Invoice Number')
	order_type = models.CharField(max_length=150,blank=True,null=True,verbose_name='Order Type')
	outlet = models.CharField(max_length=150,null=True, blank=True, verbose_name='Outlet')
	payment_mode = models.CharField(max_length=150,blank=True,null=True,verbose_name='Payment Mode')
	rider_name = models.CharField(max_length=150,null=True, blank=True, verbose_name='Rider Name')
	rider_number = models.CharField(max_length=150,null=True, blank=True, verbose_name='Rider Number')
	source = models.CharField(max_length=150,null=True, blank=True, verbose_name='Source')
	status_name = models.CharField(max_length=150,null=True, blank=True, verbose_name='Status Name')
	sub_total = models.FloatField(null=True, blank=True, verbose_name='Sub Total')
	time = models.TimeField(auto_now=False, auto_now_add=False, null=True,blank=True,
											verbose_name="Time")
	total = models.FloatField(blank=True,null=True,verbose_name='Total')
	subtotal = models.FloatField(blank=True,null=True,verbose_name='Sub Total')
	total_tax = models.FloatField(blank=True,null=True,verbose_name='Total Tax')
	diff_amount = models.FloatField(blank=True,null=True,verbose_name='Difference Amount')
	user_name = models.CharField(max_length=150,null=True, blank=True, verbose_name='User Name')
	company = models.ForeignKey(Company,blank=True,null=True, related_name='SushiyaCustomer_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})



	class Meta:
		verbose_name = 'Sushiya POS Management'
		verbose_name_plural = ' Sushiya POS Management'

	def __str__(self):
		return self.source




















