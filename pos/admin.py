from django.contrib import admin
from django.db.models import Q
from pos.models import POSOrder
import datetime



def make_active(modeladmin, request, queryset):
	queryset.update(active_status='1',updated_at=datetime.datetime.now())
make_active.short_description = "Move Items to Active"

def make_deactive(modeladmin, request, queryset):
	queryset.update(active_status='0',updated_at=datetime.datetime.now())
make_deactive.short_description = "Move Items to Deactive"


class POSOrderAdmin(admin.ModelAdmin):

	list_filter = ['date','created_on','source']

	search_fields = ['customer_name','customer_number']

	list_display = [
		'customer_name', 
		'customer_number',
		'date',
		'created_on',
		'source',
		'discount_value',
		'invoice_number',

	]


	readonly_fields = [
		'customer_name', 
		'customer_number',
		'date',
		'created_on',
		'source',
		'discount_value',
		'invoice_number',

	]

	list_per_page = 100


	def has_delete_permission(self, request, obj=None):
		return False

	def has_add_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		obj.save()

admin.site.register(POSOrder,POSOrderAdmin)