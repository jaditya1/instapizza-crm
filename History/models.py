from django.db import models
from django.contrib.auth.models import User
# from instacustomer.models import Instacustomer
from django.db.models import Count, Sum
# from configuration.models import *
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.safestring import mark_safe
from zapio.settings import MEDIA_URL
# from outletmanager.models import InstaOutletProfile
from Brands.models import Company
from Product.models import *
from django.contrib.postgres.fields import ArrayField,JSONField
from Outlet.models import OutletProfile
from discount.models import Coupon
from Orders.models import Order
from Brands.models import Company
from Outlet.models import DeliveryBoy

class CouponUsed(models.Model):
	Coupon =  models.ForeignKey(Coupon, related_name='CouponUsed_coupon',
												on_delete=models.CASCADE,verbose_name='Coupon',
												limit_choices_to={'active_status':'1'})
	customer = JSONField(blank=True,null=True,verbose_name="Customer Details")
	order_id = models.ForeignKey(Order, related_name='CouponUsed_order',
												on_delete=models.CASCADE,verbose_name='Order')
	Company = models.ForeignKey(Company, related_name='CouponUsed_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	outlet = models.ForeignKey(OutletProfile, related_name='CouponUsed_OutletProfile',
												on_delete=models.CASCADE,verbose_name='Outlet',
												limit_choices_to={'active_status':'1'})
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Used At')

	class Meta:
		verbose_name ="Used Coupon"
		verbose_name_plural ="  Used Coupons"

	def __str__(self):
		return str(self.Coupon.coupon_code)


class RiderHistory(models.Model):
	Rider =  models.ForeignKey(DeliveryBoy, related_name='RiderHistory_Rider',
												on_delete=models.CASCADE,verbose_name='Rider',
												limit_choices_to={'active_status':'1'})
	order_id = models.ForeignKey(Order, related_name='RiderHistory_order',
												on_delete=models.CASCADE,verbose_name='Order')
	Company = models.ForeignKey(Company, related_name='RiderHistory_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	outlet = models.ForeignKey(OutletProfile, related_name='RiderHistory_OutletProfile',
												on_delete=models.CASCADE,verbose_name='Outlet',
												limit_choices_to={'active_status':'1'})
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Used At')

	class Meta:
		verbose_name ="Rider History"
		verbose_name_plural ="  Rider History"

	def __str__(self):
		return str(self.Rider.name)



class OutletLogs(models.Model):
	Company = models.ForeignKey(Company, related_name='OutletLog_Company',
										on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	outlet = models.ForeignKey(OutletProfile, related_name='OutletLog_OutletProfile',
												on_delete=models.CASCADE,verbose_name='Outlet',
												limit_choices_to={'active_status':'1'})
	opening_time = models.DateTimeField(auto_now_add=False, null=True,blank=True,
											verbose_name="Opening Time")
	

	closing_time = models.DateTimeField(auto_now_add=False, null=True,blank=True,
											verbose_name="Closing Time")
	auth_user = models.ForeignKey(User, on_delete=models.CASCADE,
										related_name='OutletLog_auth_user', null=True,
								  		 blank=True)
	is_open = models.BooleanField(default=1, verbose_name='Is Open')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Used At')



	class Meta:
		verbose_name ="OutletLogHistory"
		verbose_name_plural ="  OutletLog History"

	def __str__(self):
		return str(self.auth_user)