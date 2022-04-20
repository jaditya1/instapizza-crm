from django.contrib import admin
from Brands.models import Company
from datetime import datetime
from Orders.models import *
from django.contrib.admin import site
from django.forms.utils import ErrorList
from django import forms
from django.contrib.auth.models import User
from Configuration.admin import make_active, make_deactive
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from django.http import HttpResponse


def export_xls(modeladmin, request, queryset):
	import xlwt
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename=ProcessReport.xls'
	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet("OrderProcessReport")

	row_num = 0

	columns = [
		("S.No", 2000),
		("Outlet Order Id",4000),
		("Order Id", 4000),
		("Order Acceptance Time", 3000),
		("KPT", 3000),
		("KPT To Dispatch", 3000),
	]

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num][0], font_style)
		# set column width
		ws.col(col_num).width = columns[col_num][1]

	font_style = xlwt.XFStyle()
	font_style.alignment.wrap = 1

	for obj in queryset:
		row_num += 1
		row = [
			row_num,
			obj.order.outlet_order_id,
			obj.order.order_id,
			obj.order_acceptance_time,
			obj.kpt,
			obj.kpt_to_dispatch
		]
		for col_num in range(len(row)):
			ws.write(row_num, col_num, row[col_num], font_style)

	wb.save(response)
	return response

export_xls.short_description = "Export Selected to XLS"





class OrderStatusMasterAdmin(admin.ModelAdmin):
	# form = CompanyForm
	exclude = [
			'created_at',
			'updated_at',
			'active_status'
			]
	search_fields = [
		'Order_staus_name',
		]
	list_display = [
		  'Order_staus_name',
		  'active_status',
		  'can_process',
		  'created_at',
		  'updated_at'
			]
	list_filter = [
		'active_status',
		'created_at',
		'updated_at'
		]
	actions = [make_active, make_deactive]
	list_per_page = 5
	# list_display_links = None
	
	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
			obj.save()
		else:
			obj.updated_at = datetime.now()
			obj.save()

	def has_delete_permission(self, request, obj=None):
		return False

	def has_add_permission(self, request, obj=None):
		return True

class OrderMasterAdmin(admin.ModelAdmin):
	# form = InstaOutletForm
	exclude = ['is_paid','synced','is_logged']
	list_filter = ['channel_order_id','is_paid','outlet__Outletname','Company__company_name','payment_mode',
	'order_status','is_completed','has_been_here','order_source','order_type','is_aggregator',
	('order_time',DateRangeFilter)]
	search_fields = ['order_id','outlet_order_id','urban_order_id','order_description']
	list_display = ['order_id','order_time','delivery_time','payment_mode','order_status',\
					'is_aggregator','urban_order_id','channel_order_id',\
					'has_been_here','sub_total','discount_value','taxes','total_bill_value']
	# readonly_fields = ['updated_at']
	readonly_fields = ['Company','outlet','order_id','outlet_order_id','address','customer',
	'Company_outlet_details','settlement_details','delivery_boy_details',\
	'tax_detail','Aggregator_order_status',\
	# 'order_status',
	'is_aggregator','urban_order_id','payment_source','is_accepted','discount_Offers',\
	'transaction_id','packing_charge','delivery_charge','order_source','user',\
	'order_description','order_time','delivery_time','taxes','payment_mode','special_instructions',\
	'delivery_boy','sub_total','discount_value','payment_id','coupon_code','discount_name','is_paid',\
	'total_bill_value','total_items','is_completed','has_been_here','is_seen','is_rider_assign',\
	'order_type',\
	'order_cancel','cancel_responsibility','order_cancel_reason','channel_order_id']

	# 
	list_per_page = 10

	# list_display_links = None

	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			obj.updated_at = datetime.now()
		obj.save()


class OrderTrackingAdmin(admin.ModelAdmin):
	# form = InstaOutletForm
	exclude = []
	list_filter = ['Order_staus_name','created_at','order__Company__company_name',
															'order__outlet__Outletname']
	search_fields = ['order__order_id']
	list_display = ['order','Order_staus_name','created_at','updated_at']
	readonly_fields = ['updated_at']


	list_per_page = 5

	list_display_links = None

	# change_form_template = 'custom_form_outlet.html'

	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			obj.updated_at = datetime.now()
		obj.save()

class OrderProcessTimeLogAdmin(admin.ModelAdmin):
	# form = InstaOutletForm
	exclude = ['ttk']
	list_filter = ['order__Company__company_name',
	('order__order_time',DateRangeFilter),
															'order__outlet__Outletname']
	search_fields = ['order__order_id','order__outlet_order_id']
	list_display = ['order','get_outlet_order_id','order_acceptance_time','kpt','kpt_to_dispatch',
					'get_outlet_time']
	readonly_fields = ['order','order_acceptance_time','kpt','kpt_to_dispatch']


	list_per_page = 10

	ordering = ['-order__order_time']
	actions = [export_xls]
	# list_display_links = None

	# change_form_template = 'custom_form_outlet.html'

	def get_outlet_order_id(self, obj):
		return obj.order.outlet_order_id
	get_outlet_order_id.short_description = 'Outlet Order Id'
	get_outlet_order_id.admin_order_field = 'order__outlet_order_id'

	def get_outlet_time(self, obj):
		return obj.order.order_time
	get_outlet_time.short_description = 'Order Time'
	get_outlet_time.admin_order_field = 'order__order_time'

	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		obj.save()


admin.site.register(OrderStatusType,OrderStatusMasterAdmin)
admin.site.register(Order,OrderMasterAdmin)
admin.site.register(OrderTracking,OrderTrackingAdmin)
admin.site.register(OrderProcessTimeLog,OrderProcessTimeLogAdmin)




