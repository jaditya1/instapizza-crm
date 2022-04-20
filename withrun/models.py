from django.db import models
from django.contrib.auth.models import User
from Brands.models import Company
from django.contrib.postgres.fields import ArrayField,JSONField
from Outlet.models import *
from Orders.models import Order


class OrderSync(models.Model):
	Company = models.ForeignKey(Company, related_name='OrderSync_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'}) 

	outlet = models.ForeignKey(OutletProfile, related_name='OrderSync_outlet',
											on_delete=models.CASCADE,verbose_name='Outlet',
											limit_choices_to={'active_status':'1'},null=True,blank=True) 
	last_synced = models.DateTimeField(null=True,blank=True,
											verbose_name='Last Synced Date & Time')

	created_at = models.DateTimeField(auto_now_add=True,
											verbose_name='Creation Date & Time')

	class Meta:
		verbose_name = 'Withrun Order Sync'
		verbose_name_plural = '       Withrun Order Sync'

	def __str__(self):
		return str(self.Company)


class SyncOrders(models.Model):
	outlet = models.ForeignKey(OutletProfile, related_name='SyncOrders_outlet',
											on_delete=models.CASCADE,verbose_name='Outlet',
											limit_choices_to={'active_status':'1'},null=True,blank=True) 
	order = models.ForeignKey(Order, related_name='SyncOrders_order',on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True,
											verbose_name='Creation Date & Time')

	class Meta:
		verbose_name = 'Withrun Synced Orders'
		verbose_name_plural = '       Withrun Synced Orders'

	def __str__(self):
		return str(self.order)



