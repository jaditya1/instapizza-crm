from django.contrib import admin
from withrun.models import *
from datetime import datetime
from django.contrib.admin import site

# Register your models here.



class OrderSyncAdmin(admin.ModelAdmin):
	# form = BusinessTypeForm
	exclude = [
			'created_at',
			]
	# search_fields = ['username','apikey']
	list_filter = [
				'Company__company_name',
				'outlet__Outletname',
				'created_at',
				'last_synced'
				]
	list_display=[
				'Company',
				'outlet',
				'last_synced',
				'created_at', 
				]
	list_per_page = 10

	readonly_fields = ['Company','outlet','last_synced']

	def has_delete_permission(self, request, obj=None):
		return False

	def has_add_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		obj.save()

class SyncOrdersAdmin(admin.ModelAdmin):
	# form = BusinessTypeForm
	exclude = [
			'created_at',
			]
	# search_fields = ['username','apikey']
	list_filter = [
				'outlet__Outletname',
				'created_at',
				]
	list_display=[
				'outlet',
				'order',
				'created_at', 
				]
	list_per_page = 10

	readonly_fields = ['outlet','order','created_at']

	def has_delete_permission(self, request, obj=None):
		return False

	def has_add_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		obj.save()

admin.site.register(OrderSync, OrderSyncAdmin)
admin.site.register(SyncOrders, SyncOrdersAdmin)
