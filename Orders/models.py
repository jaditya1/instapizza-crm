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
from Outlet.models import OutletProfile, DeliveryBoy


class OrderStatusType(models.Model):
	Order_staus_name =  models.CharField(max_length=100,blank=True,null=True,verbose_name=
															'Order Status Name')
	color_code = models.CharField(max_length=150,blank=True,null=True,verbose_name=
															'Color Code')
	priority = models.PositiveIntegerField(null=True, blank=True, unique=True, verbose_name='Priority')
	is_delivery_boy = models.CharField(choices=(
							 ("1", "Yes"),
							 ("0", "No"),
						),max_length=100,blank=True,null=True,verbose_name='Can Assign to Delivery Boy')
	active_status = models.BooleanField(default=1, verbose_name='Is Active')
	can_process = models.BooleanField(default=1, verbose_name='Can Process')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')

	class Meta:
		verbose_name ="Order Status Type"
		verbose_name_plural ="  Order Status Type"

	def __str__(self):
		return str(self.Order_staus_name)





class Order(models.Model):
	order_id = models.CharField(max_length=150,blank=True,null=True,verbose_name=
															'Order Id')
	outlet_order_id = models.CharField(max_length=150,blank=True,null=True,verbose_name=
															'Outlet Order Id')
	channel_order_id = models.CharField(max_length=150,blank=True,null=True,verbose_name=
															'Channel Order Id')
	tax_detail = JSONField(blank=True,null=True,verbose_name="Tax Details")
	address = JSONField(blank=True,null=True,verbose_name="Address Details")
	customer = JSONField(blank=True,null=True,verbose_name="Customer Details")
	delivery_boy_details = JSONField(blank=True,null=True,verbose_name="Delivery Boy Details")
	Company_outlet_details = JSONField(blank=True,null=True,verbose_name="Company & Outlet Details")
	order_description = JSONField(blank=True,null=True,verbose_name='Order Description')
	order_time =models.DateTimeField(blank=True,null=True,verbose_name='Order Time')
	delivery_time =models.DateTimeField(blank=True,null=True,verbose_name='Delivery Time')
	taxes = models.FloatField(max_length=99999.99,blank=True,null=True,verbose_name='Tax')
	external_discount = models.FloatField(max_length=99999.99,blank=True,null=True,\
															verbose_name='External Discount')
	payment_mode = models.CharField(choices=(
											("0", "Cash on Delivery"),
											("1", "Dineout"),
											("2","Paytm"),
											("3","Razorpay"),
											("4","PayU"),
											("5","EDC"),
											("6","Mobiquik"),
											("7","Mix"),
											("8","EDC Amex"),
											("9","EDC Yes Bank"),
											("10","swiggy"),
											("11","Z Prepaid"),
											("12","S Prepaid"),
											('13',"Dunzo"),
											("14","Zomato Cash"),
											('15',"Zomato"),
											('16',"Magic Pin"),
											('17',"Easy Dinner")
											),verbose_name='Payment Mode',
											blank=True,null=True,max_length=150)
	settlement_details = JSONField(blank=True,null=True,verbose_name="Settlement Details")

	Aggregator_order_status = models.CharField(max_length=150,blank=True,null=True,verbose_name=
															'Aggregator Order Status')
	is_aggregator = models.BooleanField(default=0, verbose_name='Is Aggregator')
	urban_order_id  = models.CharField(max_length=150,blank=True,null=True,verbose_name=
															'Aggregator Order ID')
	payment_source = models.CharField(verbose_name ='Payment Source',
											blank=True,null=True,max_length=150)
	packing_charge = models.FloatField(max_length=99999.99,blank=True,null=True,verbose_name='Packing Charge')
	delivery_charge = models.FloatField(max_length=99999.99,blank=True,null=True,verbose_name='Delivery Charge')
	order_source = models.CharField(verbose_name='Order Source',
											blank=True,null=True,max_length=150)
	user = models.CharField(verbose_name='User',blank=True,null=True,max_length=150)
	order_type = models.CharField(verbose_name='Order Type',
											blank=True,null=True,max_length=150)
	order_cancel = models.CharField(max_length=255,blank=True,null=True,verbose_name=
															'Order Cancel')
	special_instructions = models.TextField(blank=True,null=True,verbose_name=
															'Special Instructions')
	order_status = models.ForeignKey(OrderStatusType,
						related_name='Order_OrderStatusType',on_delete=models.CASCADE,
		verbose_name='Order Status',limit_choices_to={'active_status': '1'}, null=True, blank=True)
	delivery_boy = models.ForeignKey(DeliveryBoy, blank=True,null=True,
											on_delete=models.CASCADE,verbose_name='Delivery Boy',
											limit_choices_to={'active_status':'1'})
	sub_total = models.FloatField(blank=True,null=True,verbose_name='Sub Total')
	discount_value = models.FloatField(blank=True,null=True,verbose_name='Discount Value')
	
	discount_name = models.CharField(max_length=150,blank=True,null=True,verbose_name=
															'Discount Name')
	
	discount_reason = models.CharField(max_length=150,blank=True,null=True,verbose_name=
															'Discount Reason')

	payment_id = models.CharField(max_length=150,blank=True,null=True,verbose_name=
															'Payment Id')

	transaction_id = models.CharField(max_length=150,blank=True,null=True,verbose_name=
															'Transaction Id')

	discount_Offers = models.CharField(max_length=150,blank=True,null=True,verbose_name=
															'Discount Offers')

	coupon_code = models.CharField(max_length=150,blank=True,null=True,verbose_name=
															'Coupon Code')
	is_paid = models.BooleanField(blank=True,null=True, verbose_name='Is Paid')
	total_bill_value =  models.FloatField(blank=True,null=True,verbose_name='Total Payable Amount')
	total_items = models.PositiveIntegerField(verbose_name='Total Items', null=True, blank=True)
	Company = models.ForeignKey(Company, related_name='Order_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	is_completed = models.BooleanField(default=0, verbose_name='Is Completed')
	outlet = models.ForeignKey(OutletProfile, related_name='Order_OutletProfile',blank=True,null=True,
												on_delete=models.CASCADE,verbose_name='Outlet',
												limit_choices_to={'active_status':'1'})
	has_been_here = models.BooleanField(default=0, verbose_name='Has Been Here')
	is_seen = models.BooleanField(default=0, verbose_name='Is Seen')
	is_accepted = models.BooleanField(default=0, verbose_name='Is Accepted')
	is_rider_assign = models.BooleanField(default=0, verbose_name='Is Rider Assign')
	order_cancel_reason =  models.CharField(max_length=150,blank=True,null=True,verbose_name=
															'Order Cancel Reason')
	cancel_responsibility =  models.CharField(max_length=150,blank=True,null=True,verbose_name=
															'Cancellation Description')
	delivery_type = models.CharField(max_length=150,blank=True,null=True,verbose_name=
															'Delivery Type')
	aggregator_payment_mode = models.CharField(blank=True,null=True,verbose_name=
											'Aggregator Payment Mode', choices=(
											("COD", "COD"),
											("Swiggy", "Swiggy"),
											("Zomato","Zomato"),),max_length=150)
	is_logged =  models.BooleanField(default=0)
	rating = models.FloatField(null=True, blank=True, verbose_name="Rating")
	synced = models.BooleanField(default=0, verbose_name='Is Synced')

	class Meta:
		verbose_name ="Order Management"
		verbose_name_plural =" Order Management"

	def __str__(self):
		return str(self.order_id)

class OrderTracking(models.Model):
	order = models.ForeignKey(Order, related_name='OrderTracking_order',
										on_delete=models.CASCADE,verbose_name='Order Tracking')
	Order_staus_name =  models.ForeignKey(OrderStatusType, related_name='OrderTracking_order_status',
										on_delete=models.CASCADE,verbose_name='Order Status')
	active_status = models.BooleanField(default=1, verbose_name='Is Active')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')
	key_person =  models.CharField(max_length=150,blank=True,null=True,verbose_name='Key Person')
	
	class Meta:
		verbose_name ="Order Tracking"
		verbose_name_plural ="  Order Tracking"

	def __str__(self):
		return str(self.Order_staus_name)


class QuantityWiseOrderProcess(models.Model):
	order = models.ForeignKey(Order, related_name='QuantityWiseOrderProcess_order',
										null=True, blank=True,on_delete=models.CASCADE,verbose_name='Order id')
	product = models.ForeignKey(Product, related_name='QuantityWiseOrderProcess_product',
									null=True, blank=True,on_delete=models.CASCADE,verbose_name='product')
	variant = models.ForeignKey(Variant, related_name='QuantityWiseOrderProcess_product',
									null=True, blank=True,on_delete=models.CASCADE,verbose_name='variant')

	quantity = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(10000),], 
						verbose_name='Priority', null=True, blank=True)
	active_status = models.BooleanField(default=0, verbose_name='Is Active')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')

	class Meta:
		verbose_name ="Order QuantityWiseOrderProcess"
		verbose_name_plural ="Order QuantityWiseOrderProcess"

	def __str__(self):
		return str(self.order)


class OrderProcessTimeLog(models.Model):
	order = models.ForeignKey(Order, related_name='OrderProcessTimeLog_order',
										on_delete=models.CASCADE,verbose_name='Order')
	order_acceptance_time = \
	models.FloatField(default=0, verbose_name="Order Acceptance Time")
	kpt = models.FloatField(default=0, verbose_name="KPT")
	kpt_to_dispatch = models.FloatField(default=0, verbose_name="KPT To Dispatch")
	ttk = models.FloatField(default=0, verbose_name="TTK")


	class Meta:
		verbose_name = "Order Process Time Log"
		verbose_name_plural = "Order Process Time Log"

	def __str__(self):
		return str(self.order)





