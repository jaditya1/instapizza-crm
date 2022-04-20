from datetime import datetime

from django.contrib import admin

from Dunzo.models import Unprocessed_Order_Quote, Processed_Order_Quote, Order_Task, Task_State_Updates, Client_details


class ClientAdmin(admin.ModelAdmin):
	exclude = ['updated_at','created_at']
	list_display=['client_id','client_token']
	readonly_fields = ['client_id','client_token',]
	def has_delete_permission(self, request, obj=None):
		return False
	def save_model(self, request, obj, form, change):
		obj.save()
	def has_add_permission(self, request, obj=None):
		return False


class UserUnprocessedOrderQuoteAdmin(admin.ModelAdmin):
	exclude = ['updated_at']
	list_display=['order_quote_id','raw_api_response','created_at']
	readonly_fields = ['order_quote_id','raw_api_response','created_at']

	search_fields = [
	  'order_quote_id',
	  ]

	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

class UserProcessedOrderQuoteAdmin(admin.ModelAdmin):
	exclude = ['updated_at']
	list_display=['order_quote_id','category_id','distance','estimated_price','eta','created_at']
	readonly_fields = ['order_quote_id','category_id','distance','estimated_price','eta','created_at']

	search_fields = [
	  'order_quote_id__order_id',
	  ]

	list_filter = ['category_id']

	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

class OrderTaskAdmin(admin.ModelAdmin):
	exclude = ['updated_at']
	list_display=['order_id','task_id','state','request_id','eta']
	readonly_fields = ['reference_id','order_id','task_id','state','request_id','eta','created_at',\
						'estimated_price']

	search_fields = [
	 'order_id__order_id','task_id'
	  ]

	list_filter = ['state']

	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

class AdminTaskStateUpdates(admin.ModelAdmin):
	list_display=['task_id','event_type','event_id','reference_id','state','eta','price','total_time',
				  'cancelled_by','cancellation_reason','runner']
	readonly_fields = ['task_id','event_type','event_id','reference_id','state','eta','price',
					   'total_time','cancelled_by','cancellation_reason','runner','updated_at','created_at']

	search_fields = [
	 'task_id'
	  ]

	list_filter = ['event_type','state']

	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False


admin.site.register(Client_details, ClientAdmin)
admin.site.register(Unprocessed_Order_Quote, UserUnprocessedOrderQuoteAdmin)
admin.site.register(Order_Task, OrderTaskAdmin)
admin.site.register(Processed_Order_Quote, UserProcessedOrderQuoteAdmin)
admin.site.register(Task_State_Updates, AdminTaskStateUpdates)

