from django.db import models
from Brands.models import Company
from Outlet.models import OutletProfile
from django.contrib.postgres.fields import ArrayField,JSONField
from Product.models import ProductCategory, Product, Tag, Variant, ProductsubCategory, AddonDetails,\
Addons
from datetime import datetime
# Create your models here.

class UrbanCred(models.Model):
	company = models.ForeignKey('Brands.Company', related_name='UrbanCred_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	username = models.CharField(max_length=50, null=True, blank=True, verbose_name="User Name")
	apikey = models.CharField(max_length=50, null=True, blank=True, verbose_name="API Key")
	active_status = models.BooleanField(default=1, verbose_name='Is Active')
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																			'Updation Date & Time')

	class Meta:
		verbose_name = "    Account Credential"
		verbose_name_plural = "                    Account Credential"

	def __str__(self):
		return str(self.company)


class EventTypes(models.Model):
	company = models.ForeignKey('Brands.Company', related_name='EventTypes_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	event_type = models.CharField(max_length=255, verbose_name="Event Type")
	event_type_desc = \
	models.CharField(max_length=255,null=True, blank=True, verbose_name="Event Type Description")
	active_status = models.BooleanField(default=1, verbose_name='Is Active')
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																			'Updation Date & Time')

	class Meta:
		verbose_name = "    Event Type"
		verbose_name_plural = "                   Event Types"
		unique_together = ('company', 'event_type')

	def __str__(self):
		return str(self.event_type)


class webHooks(models.Model):
	company = models.ForeignKey('Brands.Company', related_name='webHooks_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	callbackurl = models.CharField(max_length=255,verbose_name="Call Back Url")
	event_type = models.ForeignKey(EventTypes, related_name='webHooks_event_type',
												on_delete=models.CASCADE,verbose_name='Event Type',
												limit_choices_to={'active_status':'1'})
	api_response = JSONField(blank=True,null=True)
	error_api_response = JSONField(blank=True,null=True)
	active_status = models.BooleanField(default=1, verbose_name='Is Active')
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																			'Updation Date & Time')

	class Meta:
		verbose_name = "    WebHook Setting"
		verbose_name_plural = "                  WebHook Setting"
		unique_together = ('company', 'event_type')

	def __str__(self):
		return str(self.company)


class APIReference(models.Model):
	company = models.ForeignKey('Brands.Company', related_name='APIReference_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	outlet = models.ForeignKey(OutletProfile, related_name='APIReference_outlet',
												on_delete=models.CASCADE,verbose_name='Outlet',
												limit_choices_to={'active_status':'1'},\
												blank=True,null=True)
	event_type = models.ForeignKey(EventTypes, related_name='APIReference_event_type',
												on_delete=models.CASCADE,verbose_name='Event Type',
												limit_choices_to={'active_status':'1'})
	ref_id = models.CharField(max_length=255,verbose_name="API Reference Id")
	api_response = JSONField(blank=True,null=True)
	error_api_response = JSONField(blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																	'Updation Date & Time')

	class Meta:
		verbose_name = "   API Service Status"
		verbose_name_plural = "                 API Service Status"

	def __str__(self):
		return str(self.ref_id)

class MenuPayload(models.Model):
	company = models.ForeignKey('Brands.Company', related_name='MenuPayload_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	outlet = models.ForeignKey(OutletProfile, related_name='MenuPayload_outlet',
												on_delete=models.CASCADE,verbose_name='Outlet',
												limit_choices_to={'active_status':'1'},\
												null=True,blank=True)
	plateform = models.CharField(max_length=150,blank=True,null=True,verbose_name=
															'Plateform')
	payload = JSONField(blank=True,null=True,verbose_name='Payload')
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')

	class Meta:
		verbose_name = "   Menu Payload"
		verbose_name_plural = "                Menu Payload"

	def __str__(self):
		return str(self.company)



class RawApiResponse(models.Model):
	company = models.ForeignKey('Brands.Company', related_name='RawApiResponse_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	ref_id = models.ForeignKey(APIReference, related_name='RawApiResponse_ref',
												on_delete=models.CASCADE,verbose_name='API Reference Id',
							null=True, blank=True)
	api_response = JSONField(blank=True,null=True)
	url = models.CharField(max_length=255,verbose_name="Url of Event", null=True, blank = True)
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')

	class Meta:
		verbose_name = "   Raw ApiResponse"
		verbose_name_plural = "               Raw Api Response"

	def __str__(self):
		return str(self.company)

class OutletSync(models.Model):
	company = models.ForeignKey('Brands.Company', related_name='OutletSync_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	outlet = models.ForeignKey(OutletProfile, related_name='OutletSync_outlet',
												on_delete=models.CASCADE,verbose_name='Outlet',
												limit_choices_to={'active_status':'1'})
	ref_id = models.ForeignKey(APIReference, related_name='OutletSync_ref',
												on_delete=models.CASCADE,verbose_name='API Reference Id',
							null=True, blank=True)
	is_synced = models.BooleanField(default=0, verbose_name='Is Synced')
	urbanpiper_store_id = models.CharField(max_length=255,verbose_name="UrbanPiper Store Id",
																		null=True,blank=True)
	sync_status = models.CharField(max_length=50, choices=[
						('not_intiated','Not Initiated'), 
						('in_progress','In Progress'),
						('synced','Synced'),
							], verbose_name='Sync Status',default='not_intiated')
	urban_event = models.CharField(max_length=50, choices=[
						('updated','Store Updated'), 
						('created','Store Created'),
							], verbose_name='Event At UrbanPiper',null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	action_at = models.DateTimeField(null=True, blank=True, verbose_name=
																	'Sync Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																	'Updation Date & Time')

	class Meta:
		verbose_name = "   Outlet Sync Status"
		verbose_name_plural = "              Outlet Sync Status"

	def __str__(self):
		return str(self.outlet.Outletname)



class OrderRawApiResponse(models.Model):
	company = models.ForeignKey('Brands.Company', related_name='OrderRawApiResponse_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	sync_outlet = models.ForeignKey(OutletSync, related_name='OrderRawApiResponse_outlet',
											on_delete=models.CASCADE,verbose_name='Synced Outlet')
	api_response = JSONField(blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')

	class Meta:
		verbose_name = "   Order Relay Raw Api Response"
		verbose_name_plural = "             Order Relay Raw Api Response"

	def __str__(self):
		return str(self.company)


class OrderStatusRawApiResponse(models.Model):
	company = models.ForeignKey('Brands.Company', related_name='OrderStatusRawApi_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	sync_outlet = models.ForeignKey(OutletSync, related_name='OrderStatusRawApi_outlet',
											on_delete=models.CASCADE,verbose_name='Synced Outlet')
	api_response = JSONField(blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')

	class Meta:
		verbose_name = "   Order Status Update Raw Api Response"
		verbose_name_plural = "            Order Status Update Raw Api Response"

	def __str__(self):
		return str(self.company)


class RiderStatusRawApiResponse(models.Model):
	company = models.ForeignKey('Brands.Company', related_name='RiderStatusRawApi_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	sync_outlet = models.ForeignKey(OutletSync, related_name='RiderStatusRawApi_outlet',
											on_delete=models.CASCADE,verbose_name='Synced Outlet')
	api_response = JSONField(blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')

	class Meta:
		verbose_name = "   Rider Status Update Raw Api Response"
		verbose_name_plural = "           Rider Status Update Raw Api Response"

	def __str__(self):
		return str(self.company)


class ActionSync(models.Model):
	company = models.ForeignKey('Brands.Company', related_name='ActionSync_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	sync_outlet = models.ForeignKey(OutletSync, related_name='ActionSync_outlet',
												on_delete=models.CASCADE,verbose_name='Synced Outlet',
											)
	ref_id = models.ForeignKey(APIReference, related_name='ActionSync_ref',
												on_delete=models.CASCADE,verbose_name='API Reference Id',
							null=True, blank=True)
	is_enabled = models.BooleanField(default=0, verbose_name='Is Synced')
	urban_event = models.CharField(max_length=50, choices=[
						('enabled','Store Enabled'), 
						('disabled','Store Disabled'),
							], verbose_name='Event At UrbanPiper',null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																	'Updation Date & Time')

	class Meta:
		verbose_name = "   Synced Outlet Status"
		verbose_name_plural = "          Synced Outlet Status"

	def __str__(self):
		return str(self.is_enabled)


class CatSync(models.Model):
	company = models.ForeignKey('Brands.Company', related_name='CatSync_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	category = models.ForeignKey('Product.ProductCategory', related_name='CatSync_category',
												on_delete=models.CASCADE,verbose_name='Category',
												limit_choices_to={'active_status':'1'})
	outlet_map = ArrayField(models.TextField(),null=True, blank=True, \
											verbose_name="Outlet Mapped Ids")
	active_status = models.BooleanField(default=0, verbose_name='Is Active')
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																	'Updation Date & Time')

	class Meta:
		verbose_name = "   Synced Category"
		verbose_name_plural = "         Synced Categories"

	def __str__(self):
		return str(self.category.category_name)




class SubCatSync(models.Model):
	company = models.ForeignKey('Brands.Company', related_name='SubCatSync_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	sub_category = models.ForeignKey('Product.ProductsubCategory', related_name='SubCatSync_subcategory',
												on_delete=models.CASCADE,verbose_name='Sub Category',
												limit_choices_to={'active_status':'1'})
	outlet_map = ArrayField(models.TextField(),null=True, blank=True, \
											verbose_name="Outlet Mapped Ids")
	active_status = models.BooleanField(default=0, verbose_name='Is Active')
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																	'Updation Date & Time')

	class Meta:
		verbose_name = "   Synced Sub Category"
		verbose_name_plural = "        Synced Sub Categories"

	def __str__(self):
		return str(self.sub_category.subcategory_name)


class CatOutletWise(models.Model):
	sync_cat = models.ForeignKey(CatSync, related_name='CatOutletWise_CatSync',
										on_delete=models.CASCADE,verbose_name='Synced Category',
											)
	sync_outlet = models.ForeignKey(OutletSync, related_name='CatOutletWise_outlet',
										on_delete=models.CASCADE,verbose_name='Synced Outlet',
					)
	urbanpiper_id = models.CharField(max_length=150,blank=True,null=True,verbose_name=
															'UrbanPiper Id')
	urban_event = models.CharField(max_length=50, choices=[
						('created','Category Created'), 
						('updated','Category Updated'),
							], verbose_name='Event At UrbanPiper',null=True, blank=True)
	sync_status = models.CharField(max_length=50, choices=[
						('not_intiated','Not Initiated'), 
						('in_progress','In Progress'),
						('synced','Synced'),
						], verbose_name='Sync Status',default='not_intiated')
	is_enabled = models.BooleanField(default=0, verbose_name='Is Synced')
	is_available = models.BooleanField(default=0, verbose_name='Is Available')
	priority = models.PositiveIntegerField(null=True, blank=True, verbose_name='Priority')
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																	'Updation Date & Time')

	class Meta:
		verbose_name = "   Synced Outlet Wise Category"
		verbose_name_plural = "       Synced Outlet Wise Categories"

	def __str__(self):
		return str(self.sync_cat)


class SubCatOutletWise(models.Model):
	sync_sub_cat = models.ForeignKey(SubCatSync, related_name='subCatOutletWise_SubCatSync',
										on_delete=models.CASCADE,verbose_name='Synced Sub Category',
											)
	sync_outlet = models.ForeignKey(OutletSync, related_name='sub_CatOutletWise_outlet',
										on_delete=models.CASCADE,verbose_name='Synced Outlet',
					)
	urbanpiper_id = models.CharField(max_length=150,blank=True,null=True,verbose_name=
															'UrbanPiper Id')
	urban_event = models.CharField(max_length=50, choices=[
						('created','Sub Category Created'), 
						('updated','Sub Category Updated'),
							], verbose_name='Event At UrbanPiper',null=True, blank=True)
	sync_status = models.CharField(max_length=50, choices=[
						('not_intiated','Not Initiated'), 
						('in_progress','In Progress'),
						('synced','Synced'),
						], verbose_name='Sync Status',default='not_intiated')
	is_enabled = models.BooleanField(default=0, verbose_name='Is Synced')
	is_available = models.BooleanField(default=0, verbose_name='Is Available')
	priority = models.PositiveIntegerField(null=True, blank=True, verbose_name='Priority')
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																	'Updation Date & Time')

	class Meta:
		verbose_name = "   Synced Outlet Wise Sub Category"
		verbose_name_plural = "      Synced Outlet Wise Sub Categories"

	def __str__(self):
		return str(self.sync_sub_cat)


class ProductSync(models.Model):
	company = models.ForeignKey('Brands.Company', related_name='ProductSync_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	category = models.ForeignKey('Product.ProductCategory', related_name='ProductSync_category',
												on_delete=models.CASCADE,verbose_name='Category',
												limit_choices_to={'active_status':'1'})
	sub_category = models.ForeignKey('Product.ProductsubCategory', \
												related_name='ProductSync_sub_category',
												on_delete=models.CASCADE,verbose_name='Sub Category',
												limit_choices_to={'active_status':'1'},\
												blank=True,null=True)
	product = models.ForeignKey('Product.Product', related_name='ProductSync_product',
												on_delete=models.CASCADE,verbose_name='Product',
												limit_choices_to={'active_status':'1'})
	variant = models.ForeignKey('Product.Variant', related_name='ProductSync_Variant',
												on_delete=models.CASCADE,verbose_name='Variant',
												limit_choices_to={'active_status':'1'},
												null=True, blank=True)
	urbanpiper_id = models.CharField(max_length=150,blank=True,null=True,verbose_name=
															'UrbanPiper Id')
	zomato_crust_id = models.ForeignKey('Product.AddonDetails', related_name='ProductSync_AddonDetails',
												on_delete=models.CASCADE,verbose_name='Zomato Crust Id',
												limit_choices_to={'active_status':'1'},
												null=True, blank=True)
	price = models.FloatField(blank=True,null=True,verbose_name='Product Price')
	discount_price = models.FloatField(blank=True,null=True,verbose_name='Discount Product Price')
	addpn_grp_association = ArrayField(models.TextField(), blank=True,null=True)
	outlet_map = ArrayField(models.TextField(),null=True, blank=True, \
											verbose_name="Outlet Mapped Ids")
	active_status = models.BooleanField(default=0, verbose_name='Is Active')
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																	'Updation Date & Time')

	class Meta:
		verbose_name = "   Synced Product"
		verbose_name_plural = "      Synced Products"

	def __str__(self):
		if self.variant == None:
			return str(self.product.product_name)
		else:
			return str(self.product.product_name+" | "+self.variant.variant)



class ProductOutletWise(models.Model):
	sync_product = models.ForeignKey(ProductSync, related_name='ProductOutletWise_ProductSync',
										on_delete=models.CASCADE,verbose_name='Synced Product',
											)
	sync_outlet = models.ForeignKey(OutletSync, related_name='ProductOutletWise_outlet',
										on_delete=models.CASCADE,verbose_name='Synced Outlet',
											)
	urban_event = models.CharField(max_length=50, choices=[
						('created','Product Created'), 
						('updated','Product Updated'),
							], verbose_name='Event At UrbanPiper',null=True, blank=True)
	sync_status = models.CharField(max_length=50, choices=[
						('not_intiated','Not Initiated'), 
						('in_progress','In Progress'),
						('synced','Synced'),
						], verbose_name='Sync Status',default='not_intiated')
	is_enabled = models.BooleanField(default=0, verbose_name='Is Synced')
	is_available = models.BooleanField(default=0, verbose_name='Is Available')
	product_status = models.CharField(max_length=50, choices=[
						('enabled','Enabled'), 
						('disabled','Disabled'),
						('in_progress','In Progress'),
						], verbose_name='Product Status',default='enabled')
	active_status = models.BooleanField(default=0, verbose_name='Is Active')
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																	'Updation Date & Time')

	class Meta:
		verbose_name = "   Synced Outlet Wise Product"
		verbose_name_plural = "    Synced Outlet Wise Products"

	def __str__(self):
		return str(self.sync_product)


class UrbanOrders(models.Model):
	order_id = models.CharField(max_length=150,blank=True,null=True,verbose_name=
															'Order Id',db_index=True)
	channel_order_id = models.CharField(max_length=150,blank=True,null=True,verbose_name=
															'Channel Order Id')
	customer_address = JSONField(blank=True,null=True,verbose_name="Customer Address Details")
	customer_data = JSONField(blank=True,null=True,verbose_name="Customer Details")
	next_states = \
	ArrayField(models.TextField(),null=True, blank=True, verbose_name="Next Possible Status")
	next_state =\
	models.CharField(max_length=150,blank=True,null=True,verbose_name=
															'Next Expected State')
	order_state = models.CharField(max_length=150,blank=True,null=True,verbose_name=
															'Current State')
	source = models.CharField(max_length=150,blank=True,null=True,verbose_name=
															'Channel')
	order_description = JSONField(blank=True,null=True,verbose_name='Order Description')
	total_items = models.PositiveIntegerField(verbose_name='Total Items', null=True, blank=True)
	discount_value = models.FloatField(blank=True,null=True,verbose_name='Discount Value')
	sub_total = models.FloatField(blank=True,null=True,verbose_name='Sub Total')
	total_bill_value =  models.FloatField(blank=True,null=True,verbose_name='Total Payable Amount')
	packing_charge = \
	models.FloatField(max_length=99999.99,blank=True,null=True,verbose_name='Packing Charge')
	delivery_charge = \
	models.FloatField(max_length=99999.99,blank=True,null=True,verbose_name='Delivery Charge')
	order_level_total_taxes = \
	models.FloatField(max_length=99999.99,blank=True,null=True,verbose_name='Order level Total Tax')
	total_tax = \
	models.FloatField(max_length=99999.99,blank=True,null=True,verbose_name='Total Tax')
	external_discount = \
	models.FloatField(max_length=99999.99,blank=True,null=True,verbose_name='External Discount')
	order_level_total_charges = \
	models.FloatField(max_length=99999.99,blank=True,null=True,verbose_name='Total Charge')
	item_level_total_charges = \
	models.FloatField(max_length=99999.99,blank=True,null=True,verbose_name='Total Charge Item Level')
	item_level_total_taxes = \
	models.FloatField(max_length=99999.99,blank=True,null=True,verbose_name='Total Tax Item Level')
	order_type = \
	models.CharField(max_length=150,blank=True,null=True,verbose_name=
															'Order Type')
	final_payment = JSONField(blank=True,null=True,verbose_name="Final Payment")
	coupon_code = models.CharField(max_length=150,blank=True,null=True,verbose_name=
															'Coupon Code')
	special_instructions = models.TextField(blank=True,null=True,verbose_name=
														'Special Instructions')
	Company = models.ForeignKey(Company, related_name='UrbanOrders_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	outlet = models.ForeignKey(OutletProfile, related_name='UrbanOrders_OutletProfile',blank=True,null=True,
												on_delete=models.CASCADE,verbose_name='Outlet',
												limit_choices_to={'active_status':'1'})
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																	'Updation Date & Time')


	class Meta:
		verbose_name ="Urban Order Management"
		verbose_name_plural ="   Urban Order Management"

	def __str__(self):
		return str(self.order_id)



class zomatoMenuTemporaryAddonData(models.Model):
	zomato_product_id = models.CharField(max_length=150, \
						verbose_name='Zomato Product Id',null=True, blank=True)
	addon_grp = models.CharField(max_length=150, \
						verbose_name='Zomato Addon Group Id',null=True, blank=True)
	

	class Meta:
		verbose_name = "   zomatoMenuTemporaryAddonData"
		verbose_name_plural = "    zomatoMenuTemporaryAddonData"

	def __str__(self):
		return str(self.zomato_product_id)


class zomatoMenuTemporaryItemData(models.Model):
	zomato_product_id = models.CharField(max_length=150, \
						verbose_name='Zomato Product Id',null=True, blank=True)
	is_size = models.BooleanField(default=0, verbose_name='Is Size')
	

	class Meta:
		verbose_name = "   zomatoMenuTemporaryItemData"
		verbose_name_plural = "    zomatoMenuTemporaryItemData"

	def __str__(self):
		return str(self.zomato_product_id)


class zomatoMenuTempOptionData(models.Model):
	zomato_product_id = models.CharField(max_length=150, \
						verbose_name='Zomato Product Id',null=True, blank=True)
	

	class Meta:
		verbose_name = "   zomatoMenuTempOptionData"
		verbose_name_plural = "    zomatoMenuTempOptionData"

	def __str__(self):
		return str(self.zomato_product_id)


class zomatoMenuTempAddonGrpData(models.Model):
	zomato_addon_grp_id = models.CharField(max_length=150, \
						verbose_name='Zomato Addon Group Id',null=True, blank=True)
	

	class Meta:
		verbose_name = "   zomatoMenuTempAddonGrpData"
		verbose_name_plural = "    zomatoMenuTempAddonGrpData"

	def __str__(self):
		return str(self.zomato_addon_grp_id)


class zomatoMenuTempAllAddonData(models.Model):
	zomato_addon_grp_id = models.CharField(max_length=150, \
						verbose_name='Zomato Addon Group Id',null=True, blank=True)
	zomato_addon_id = models.CharField(max_length=150, \
						verbose_name='Zomato Addon Id',null=True, blank=True)

	class Meta:
		verbose_name = "   zomatoMenuTempAllAddonData"
		verbose_name_plural = "    zomatoMenuTempAllAddonData"

	def __str__(self):
		return str(self.zomato_addon_grp_id)


class TempzomatoNestedCrust(models.Model):
	zomato_addon_crust_grp_id = models.CharField(max_length=150, \
						verbose_name='Zomato Addon Crust Group Id',null=True, blank=True)
	zomato_addon_id = models.CharField(max_length=150, \
						verbose_name='Zomato Addon Id',null=True, blank=True)
	nested_grp_ids = ArrayField(models.TextField(),null=True, blank=True, verbose_name="Nested Mapped Ids")

	class Meta:
		verbose_name = "   TempzomatoNestedCrust"
		verbose_name_plural = "    TempzomatoNestedCrust"

	def __str__(self):
		return str(self.zomato_addon_crust_grp_id)


class SubCatOutletWiseAddonGroup(models.Model):
	outlet = models.ForeignKey(OutletProfile, related_name='AddonGroup_OutletProfile', blank=True, null=True,
							   on_delete=models.CASCADE, verbose_name='Outlet',
							   limit_choices_to={'active_status': '1'})
	addon_group = models.ForeignKey(AddonDetails, related_name='addon_grouping',
									on_delete=models.CASCADE, verbose_name='Add-On Group',
									limit_choices_to={'active_status': '1'}, null=True, blank=True)
	is_available = models.BooleanField(default=1, verbose_name='Is Accepted')
	active_status = models.BooleanField(default=1, verbose_name='Is Active')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = "Synced Outlet Wise Addon Groups"
		verbose_name_plural = "Synced Outlet Wise Addon Groups"

	def __str__(self):
		return str(self.outlet)

class SubCatOutletWiseAddons(models.Model):
	outlet = models.ForeignKey(OutletProfile, related_name='Addon_OutletProfile', blank=True, null=True,
							   on_delete=models.CASCADE, verbose_name='Outlet',
							   limit_choices_to={'active_status': '1'})
	addon_id = models.ForeignKey(Addons, related_name='addon_id',
									on_delete=models.CASCADE, verbose_name='Add-On Group',
									limit_choices_to={'active_status': '1'}, null=True, blank=True)
	is_available = models.BooleanField(default=1, verbose_name='Is Accepted')
	active_status = models.BooleanField(default=1, verbose_name='Is Active')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = "Synced Outlet Wise Addons"
		verbose_name_plural = "Synced Outlet Wise Addons"

	def __str__(self):
		return str(self.outlet)


class LiveOrderLog(models.Model):
	request_data = JSONField(blank=True,null=True,verbose_name='Request Data')
	response_data = JSONField(blank=True,null=True,verbose_name='Response Data')
	run_time = models.FloatField(blank=True,null=True,verbose_name='Execution Time in MS')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')


	class Meta:
		verbose_name = "Live Order Log"
		verbose_name_plural = "Live Order Log"

	def __str__(self):
		return str(self.id)


class OrderStatusLog(models.Model):
	request_data = JSONField(blank=True,null=True,verbose_name='Request Data')
	response_data = JSONField(blank=True,null=True,verbose_name='Response Data')
	run_time = models.FloatField(blank=True,null=True,verbose_name='Execution Time in MS')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')


	class Meta:
		verbose_name = "Order Status Update Log"
		verbose_name_plural = "Order Status Update Log"

	def __str__(self):
		return str(self.id)


class RiderStatusLog(models.Model):
	request_data = JSONField(blank=True,null=True,verbose_name='Request Data')
	response_data = JSONField(blank=True,null=True,verbose_name='Response Data')
	run_time = models.FloatField(blank=True,null=True,verbose_name='Execution Time in MS')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')


	class Meta:
		verbose_name = "Rider Status Update Log"
		verbose_name_plural = "Rider Status Update Log"

	def __str__(self):
		return str(self.id)



