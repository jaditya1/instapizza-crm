from django.contrib import admin
from urbanpiper.models import *
from datetime import datetime
from django.contrib.admin import site
from Configuration.admin import make_active,make_deactive
from .hooks import webhooksubscribe,webhook_update
from django.http import HttpResponse
from Orders.models import Order
from .custom_action import export_xls, sync_order
from .export_product import export_product_xls


def make_not_initiated(modeladmin, request, queryset):
		queryset.update(sync_status='not_intiated',urban_event=None,ref_id=None,\
										updated_at=datetime.now(),action_at=None,is_synced=0)
make_not_initiated.short_description = "Shift Selected to Not Initiated status"

class UrbanCredAdmin(admin.ModelAdmin):
	# form = BusinessTypeForm
	exclude = [
			'active_status',
			'created_at',
			'updated_at',
			]
	search_fields = ['username','apikey']
	list_filter = [
				'active_status',
				'created_at', 
				'updated_at'
				]
	list_display=[
				'company',
				'username',
				'apikey',
				'active_status',
				'created_at', 
				'updated_at',
				]
	actions = [
			make_active,
			make_deactive,
			]
	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_by = request.user
		else:
			obj.updated_by = request.user
			obj.updated_at = datetime.now()
		obj.save()



class EventTypesAdmin(admin.ModelAdmin):
	# form = BusinessTypeForm
	exclude = [
			'active_status',
			'created_at',
			'updated_at',
			]
	search_fields = ['event_type']
	list_filter = [
				'company__company_name',
				'active_status',
				'created_at', 
				'updated_at'
				]
	list_display=[
				'company',
				'event_type',
				'event_type_desc', 
				'active_status',
				'created_at'
				]
	actions = [
			make_active,
			make_deactive,
			]
	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			obj.updated_at = datetime.now()
		obj.save()


class webHooksAdmin(admin.ModelAdmin):
	# form = BusinessTypeForm
	exclude = [
			'active_status',
			'created_at',
			'updated_at',
			]
	# search_fields = ['event_type']
	list_filter = [
				'company__company_name',
				'active_status',
				'event_type__event_type',
				'created_at', 
				'updated_at'
				]
	list_display=[
				'company',
				'callbackurl',
				'event_type', 
				'active_status',
				'created_at'
				]
	actions = [
			make_active,
			make_deactive,
			]
	readonly_fields = ['api_response','error_api_response']
	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			res = webhooksubscribe(obj.company_id,obj.event_type.event_type,obj.callbackurl)
			if "status" in res:
				if res != None and  res["status"]!="error":
					obj.api_response = res
				else:
					obj.error_api_response = res
			else:
				obj.error_api_response = res
			obj.created_at = datetime.now()
		else:
			res = webhook_update(obj)
			if "status" in res:
				if res != None and res["status"]!="error":
					obj.api_response = res
				else:
					obj.error_api_response = res
			else:
				obj.error_api_response = res
			obj.updated_at = datetime.now()
		obj.save()

class APIReferenceAdmin(admin.ModelAdmin):
	# form = BusinessTypeForm
	exclude = [
			'created_at',
			'updated_at',
			]
	# search_fields = ['event_type']
	list_filter = [
				'company__company_name',
				'outlet__Outletname',
				'event_type__event_type',
				'created_at', 
				'updated_at'
				]
	list_display=[
				'company',
				'outlet',
				'ref_id',
				'event_type',
				'created_at',
				'updated_at'
				]
	# actions = [
	# 		make_active,
	# 		make_deactive,
	# 		]

	readonly_fields = ['outlet','api_response','error_api_response','company','ref_id','event_type']
	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return True

	def has_add_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			obj.updated_at = datetime.now()
		obj.save()


class OutletSyncAdmin(admin.ModelAdmin):
	# form = BusinessTypeForm
	exclude = [
			'created_at',
			'updated_at',
			]
	# search_fields = ['event_type']
	list_filter = [
				'company__company_name',
				'outlet__Outletname',
				'created_at', 
				'updated_at',
				'sync_status',
				'is_synced',
				'urban_event',
				'action_at'
				]
	list_display=[
				'company',
				'outlet',
				'ref_id',
				'is_synced',
				'sync_status',
				'urban_event',
				'created_at',
				'action_at',
				'updated_at',
				]
	actions = [
			make_not_initiated,
			]

	readonly_fields = ['company','outlet','ref_id',
				#'is_synced','urbanpiper_store_id','sync_status',
				'urban_event','action_at']

	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return True

	def has_add_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			obj.updated_at = datetime.now()
		obj.save()

class ActionSyncAdmin(admin.ModelAdmin):
	# form = BusinessTypeForm
	exclude = [
			'created_at',
			'updated_at'
			]
	# search_fields = ['event_type']
	list_filter = [
				'company__company_name',
				'is_enabled',
				'urban_event',
				'created_at',
				'sync_outlet__outlet__Outletname'
				]
	list_display=[
				'company',
				'sync_outlet',
				'ref_id',
				'is_enabled',
				'urban_event',
				'created_at'
				]
	# actions = [
	# 		make_active,
	# 		make_deactive,
	# 		]

	readonly_fields = ['company','sync_outlet','ref_id','is_enabled', 'urban_event', 'created_at']

	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return True

	def has_add_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			pass
		obj.save()


class RawApiResponseAdmin(admin.ModelAdmin):
	# form = BusinessTypeForm
	exclude = [
			'created_at',
			]
	search_fields = ['api_response']
	list_filter = [
				'company__company_name',
				'created_at'
				]
	list_display=[
				'company',
				'url',
				'created_at'
				]
	# actions = [
	# 		make_active,
	# 		make_deactive,
	# 		]

	readonly_fields = ['company','ref_id','api_response','url']

	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return True

	def has_add_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			pass
		obj.save()


class OrderRawApiResponseAdmin(admin.ModelAdmin):
	# form = BusinessTypeForm
	exclude = [
			'created_at',
			]
	search_fields = ['api_response']
	list_filter = [
				'company__company_name',
				'sync_outlet__outlet__Outletname',
				'created_at'
				]
	list_display=[
				'company',
				'sync_outlet',
				'created_at'
				]
	# actions = [
	# 		make_active,
	# 		make_deactive,
	# 		]

	readonly_fields = ['company','sync_outlet','api_response']

	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return True

	def has_add_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			pass
		obj.save()


class OrderStatusRawApiResponseAdmin(admin.ModelAdmin):
	# form = BusinessTypeForm
	exclude = [
			'created_at',
			]
	search_fields = ['api_response']
	list_filter = [
				'company__company_name',
				'sync_outlet__outlet__Outletname',
				'created_at'
				]
	list_display=[
				'company',
				'sync_outlet',
				'created_at'
				]
	# actions = [
	# 		make_active,
	# 		make_deactive,
	# 		]

	readonly_fields = ['company','sync_outlet','api_response']

	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return True

	def has_add_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			pass
		obj.save()


class RiderStatusRawApiResponseAdmin(admin.ModelAdmin):
	# form = BusinessTypeForm
	exclude = [
			'created_at',
			]
	# search_fields = ['event_type']
	list_filter = [
				'company__company_name',
				'sync_outlet__outlet__Outletname',
				'created_at'
				]
	list_display=[
				'company',
				'sync_outlet',
				'created_at'
				]
	# actions = [
	# 		make_active,
	# 		make_deactive,
	# 		]

	readonly_fields = ['company','sync_outlet','api_response']

	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return True

	def has_add_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			pass
		obj.save()

class CatSyncAdmin(admin.ModelAdmin):
	# form = BusinessTypeForm
	exclude = [
			'active_status',
			'created_at',
			'updated_at'
			]
	search_fields = ['category']
	list_filter = [
				'company__company_name',
				# 'is_available',
				# 'is_enabled',
				# 'sync_status',
				'active_status',
				'created_at',
				'updated_at'
				]
	list_display=[
				'company',
				'category',
				'active_status',
				'created_at'
				]
	readonly_fields = ['company','category','outlet_map']

	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return True

	def has_add_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			obj.updated_at = datetime.now()
		obj.save()


class SubCatSyncAdmin(admin.ModelAdmin):
	# form = BusinessTypeForm
	exclude = [
			'active_status',
			'created_at',
			'updated_at'
			]
	search_fields = ['sub_category']
	list_filter = [
				'company__company_name',
				# 'is_available',
				# 'is_enabled',
				# 'sync_status',
				'active_status',
				'created_at',
				'updated_at'
				]
	list_display=[
				'company',
				'sub_category',
				'active_status',
				'created_at'
				]
	readonly_fields = ['company','sub_category','outlet_map']

	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return True

	def has_add_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			obj.updated_at = datetime.now()
		obj.save()

admin.site.register(SubCatSync, SubCatSyncAdmin)


class CatOutletWiseAdmin(admin.ModelAdmin):
	# form = BusinessTypeForm
	exclude = [
			'created_at',
			'updated_at'
			]
	# search_fields = ['category']
	list_filter = [
				'sync_outlet__outlet__Outletname',
				'sync_cat__category__category_name',
				'is_available',
				'is_enabled',
				'sync_status',
				'created_at',
				'updated_at'
				]
	list_display=[
				'sync_cat',
				'sync_outlet',
				'urban_event',
				'sync_status',
				'is_enabled',
				'is_available',
				'created_at'
				]
	readonly_fields = ['sync_cat','sync_outlet','urban_event','sync_status','is_enabled',
					'is_available']

	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return False

	def has_add_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			obj.updated_at = datetime.now()
		obj.save()


class SubCatOutletWiseAdmin(admin.ModelAdmin):
	# form = BusinessTypeForm
	exclude = [
			'created_at',
			'updated_at'
			]
	# search_fields = ['category']
	list_filter = [
				'sync_outlet__outlet__Outletname',
				'sync_sub_cat__sub_category__subcategory_name',
				'is_available',
				'is_enabled',
				'sync_status',
				'created_at',
				'updated_at'
				]
	list_display=[
				'sync_sub_cat',
				'sync_outlet',
				'urban_event',
				'sync_status',
				'is_enabled',
				'is_available',
				'created_at'
				]
	readonly_fields = ['sync_sub_cat','sync_outlet','urban_event','sync_status','is_enabled',
					'is_available']

	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return False

	def has_add_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			obj.updated_at = datetime.now()
		obj.save()

admin.site.register(SubCatOutletWise, SubCatOutletWiseAdmin)

class ProductSyncAdmin(admin.ModelAdmin):
	# form = BusinessTypeForm
	exclude = [
			'active_status',
			'created_at',
			'updated_at'
			]
	search_fields = ['product__product_name',"id"]
	list_filter = [
				'company__company_name',
				'product__product_name',
				'variant__variant',
				'active_status',
				'created_at',
				'updated_at',
				# 'active_status'
				]
	list_display=[
				'company',
				'category',
				'sub_category',
				'zomato_crust_id',
				'product',
				'variant',
				'active_status',
				'price',
				'discount_price'
				]
	readonly_fields = ['company','category','product','variant',
	'price','discount_price','addpn_grp_association','outlet_map']

	

	list_per_page = 10

	actions = [
			export_xls,export_product_xls,make_active,make_deactive
			]

	def has_delete_permission(self, request, obj=None):
		return False

	def has_add_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			obj.updated_at = datetime.now()
		obj.save()

class ProductOutletWiseAdmin(admin.ModelAdmin):
	# form = BusinessTypeForm
	exclude = [
			'created_at',
			'updated_at'
			]
	search_fields = ['sync_product__product__product_name']
	list_filter = [
				'sync_outlet__outlet__Outletname',
				'is_available',
				'product_status',
				'is_enabled',
				'sync_status',
				'urban_event',
				'active_status',
				'created_at',
				'updated_at'
				]
	list_display=[
				'sync_product',
				'sync_outlet',
				'urban_event',
				'sync_status',
				'is_enabled',
				'is_available',
				'active_status',
				'product_status',
				'created_at'
				]
	readonly_fields = ['sync_product','sync_outlet','urban_event','sync_status','is_enabled',
					'is_available','product_status']

	actions = [
			make_active,
			make_deactive,
			]

	list_per_page = 10



	def has_delete_permission(self, request, obj=None):
		return False

	def has_add_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			obj.updated_at = datetime.now()
		obj.save()


class UrbanOrdersAdmin(admin.ModelAdmin):
	# form = BusinessTypeForm
	exclude = [
			'created_at',
			'updated_at'
			]
	search_fields = ['order_id','channel_order_id']
	list_filter = [
				'Company__company_name',
				'outlet__Outletname',
				'source',
				'order_state',
				'order_type',
				'created_at',
				'updated_at'
				]
	list_display=[
				'order_id',
				'order_state',
				'channel_order_id',
				'next_state',
				'source',
				'order_type',
				'Company',
				'outlet',
				'created_at',
				'updated_at'
				
				]
	readonly_fields = ['order_id','channel_order_id','Company','outlet',
	'customer_address','customer_data',
	'coupon_code','next_states',
	'next_state','source','order_description','total_items',
	'discount_value','sub_total',
	'total_bill_value','packing_charge','delivery_charge','order_level_total_taxes',
	'order_level_total_charges','item_level_total_charges','item_level_total_taxes','total_tax',\
	'order_type','special_instructions',
	'final_payment']

# 
	actions = [
			sync_order,
			]
	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return False

	def has_add_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			obj.updated_at = datetime.now()
		obj.save()


class MenuPayloadAdmin(admin.ModelAdmin):
	# form = BusinessTypeForm
	exclude = [
			# 'created_at',
			]
	# search_fields = ['event_type']
	list_filter = [
				'company__company_name',
				'outlet__Outletname',
				'created_at'
				]
	list_display=[
				'company',
				'outlet',
				'created_at'
				]
	# actions = [
	# 		make_active,
	# 		make_deactive,
	# 		]

	readonly_fields = ['company','outlet','payload','created_at']

	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return False

	def has_add_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			pass
		obj.save()



admin.site.register(UrbanCred, UrbanCredAdmin)
admin.site.register(EventTypes, EventTypesAdmin)
admin.site.register(webHooks, webHooksAdmin)
admin.site.register(APIReference, APIReferenceAdmin)
admin.site.register(OutletSync, OutletSyncAdmin)
admin.site.register(RawApiResponse, RawApiResponseAdmin)
admin.site.register(ActionSync, ActionSyncAdmin)
admin.site.register(CatSync, CatSyncAdmin)
admin.site.register(ProductSync, ProductSyncAdmin)
admin.site.register(OrderRawApiResponse, OrderRawApiResponseAdmin)
admin.site.register(UrbanOrders, UrbanOrdersAdmin)
admin.site.register(OrderStatusRawApiResponse, OrderStatusRawApiResponseAdmin)
admin.site.register(RiderStatusRawApiResponse, RiderStatusRawApiResponseAdmin)
admin.site.register(CatOutletWise, CatOutletWiseAdmin)
admin.site.register(ProductOutletWise, ProductOutletWiseAdmin)
admin.site.register(MenuPayload, MenuPayloadAdmin)






class LiveOrderLogAdmin(admin.ModelAdmin):
	exclude = [
			# 'created_at',
			]
	search_fields = ['request_data']
	list_filter = [
				'created_at'
				]
	list_display=[
				'run_time',
				'response_data',
				'created_at'
				]
	readonly_fields = ['request_data','response_data','run_time','created_at']

	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return True

	def has_add_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			pass
		obj.save()


class OrderStatusLogAdmin(admin.ModelAdmin):
	exclude = [
			# 'created_at',
			]
	search_fields = ['request_data']
	list_filter = [
				'created_at'
				]
	list_display=[
				'run_time',
				'response_data',
				'created_at'
				]
	readonly_fields = ['request_data','response_data','run_time','created_at']

	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return True

	def has_add_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			pass
		obj.save()


class RiderStatusLogAdmin(admin.ModelAdmin):
	exclude = [
			# 'created_at',
			]
	search_fields = ['request_data']
	list_filter = [
				'created_at'
				]
	list_display=[
				'run_time',
				'response_data',
				'created_at'
				]
	readonly_fields = ['request_data','response_data','run_time','created_at']

	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return True

	def has_add_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			pass
		obj.save()



admin.site.register(LiveOrderLog, LiveOrderLogAdmin)
admin.site.register(OrderStatusLog, OrderStatusLogAdmin)
admin.site.register(RiderStatusLog, RiderStatusLogAdmin)