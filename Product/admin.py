from django.contrib import admin
from Product.models import *
from django import forms
from datetime import datetime
from Configuration.admin import make_active, make_deactive
from django.forms.utils import ErrorList
# from AdroitInventry.admin_validation import CityMasterForm, CountryMasterForm, StateMasterForm
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
import xlwt
from django.http import HttpResponse
from .export_product import export_xls
from .export_addons import export_xls



def addon_settings(modeladmin, request, queryset):
	for i in queryset:
		addons = i.associated_addons
		cid = i.Company_id
		if addons != None:
			for j in addons:
				q = Addons.objects.filter(Company=cid,name=j['addon_name'],addon_group=i.id)
				if q.count() == 0:
					q_create = Addons.objects.create(Company_id=cid,name=j['addon_name'],addon_group_id=i.id,\
								addon_amount=j['price'])
				else:
					q_update = q.update(name=j['addon_name'],addon_group_id=i.id,addon_amount=j['price'])
		else:
			pass
addon_settings.short_description = "Manage Associated Addons"


class CategoryMasterAdmin(admin.ModelAdmin):
	# form = CountryMasterForm
	exclude = [
	  # 'status',
		'active_status',
		'created_at',
		'updated_at',
	  ]

	list_filter = [
		'active_status',
		('created_at', DateRangeFilter),
		('updated_at', DateRangeFilter),
		'Company__company_name'
		]

	search_fields = [
	  'category_name',
	  ]

	list_display = [
	  'category_name',
	  'Company',
	  'active_status',
	  'created_at', 
	  ]

	actions = [make_active, make_deactive]
	# list_display_links = None
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



class SubCategoryMasterAdmin(admin.ModelAdmin):
	# form = CountryMasterForm
	exclude = [
	  # 'status',
		'active_status',
		'created_at',
		'updated_at',
	  ]

	list_filter = [
		'category__category_name',
		'active_status',
		('created_at', DateRangeFilter),
		('updated_at', DateRangeFilter),
		]

	search_fields = [
	  'subcategory_name',
	  ]

	list_display = [
	  'category',
	  'subcategory_name',
	  'active_status',
	  'created_at', 
	  ]
	list_display_links = None
	actions = [make_active, make_deactive]

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


class FoodTypeMasterAdmin(admin.ModelAdmin):
	# form = CountryMasterForm
	exclude = [
	  # 'status',
		'active_status',
		'created_at',
		'updated_at',
	  ]

	list_filter = [
		'active_status',
		]

	search_fields = [
	  'food_type',
	  ]

	list_display = [
	  'food_type',
	  'food_type_pic',
	  'active_status',
	  'created_at', 
	  ]

	actions = [make_active, make_deactive]

	list_per_page = 10
	list_display_links = None
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

class VariantMasterAdmin(admin.ModelAdmin):
	# form = CountryMasterForm
	exclude = [
	  # 'status',
		'active_status',
		'created_at',
		'updated_at',
	  ]

	list_filter = [
		'active_status',
		]

	search_fields = [
	  'variant',
	  ]

	list_display = [
	  'id',
	  'variant',
	  'Company',
	  'active_status',
	  'created_at', 
	  ]

	actions = [make_active, make_deactive]
	list_display_links = None
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

class AddonDetailsMasterAdmin(admin.ModelAdmin):
	# form = CountryMasterForm
	exclude = [
	  # 'status',
		'active_status',
		'created_at',
		'updated_at',
	  ]

	list_filter = [
		'Company__company_name',
		'active_status',
		]

	search_fields = [
	  'addon_gr_name',
	  ]

	list_display = [
	  'addon_gr_name',
	  'min_addons',
	  'max_addons',
	  'Company',
	  'product_variant',
	  'active_status',
	  'created_at', 
	  ]

	actions = [make_active, make_deactive, addon_settings]

	readonly_fields = ['active_status','Company','addon_gr_name','min_addons',
	'max_addons','product_variant','associated_addons']
	# list_display_links = None
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


class AddonsMasterAdmin(admin.ModelAdmin):
	# form = CountryMasterForm
	exclude = [
	  # 'status',
		'created_at',
		'updated_at'
	  ]

	list_filter = [
		'Company__company_name',
		'active_status',
		'created_at'
		]

	search_fields = [
	  'name',
	  ]

	list_display = [
	  'name',
	  'Company',
	  'addon_group',
	  'addon_amount',
	  'priority',
	  'active_status',
	  'created_at', 
	  ]

	actions = [make_active, make_deactive, export_xls]

	readonly_fields = ['Company','name',
	# 'addon_amount'
	'addon_group',
	'priority','active_status']
	# list_display_links = None
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


class ProductMasterAdmin(admin.ModelAdmin):
	# form = CountryMasterForm
	exclude = [
	  # 'status',
		'active_status',
		'created_at',
		'updated_at',
	  ]

	list_filter = [
		'active_status',
		'created_at',
		'updated_at',
		'Company__company_name'
		]

	search_fields = [
	  'product_name',
	  ]

	list_display = [
	  'product_category',
	  'product_subcategory',
	  'product_name',
	  'image',
	  'food_type',
	  'priority',
	  'active_status',
	  'created_at', 
	  ]

	actions = [export_xls, make_active, make_deactive]
	# list_display_links = None
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


class TagAdmin(admin.ModelAdmin):
	exclude = [
		'active_status',
		'created_at',
		'updated_at',
	  ]

	list_filter = [
		'active_status',
		'created_at',
		'updated_at',
		]

	search_fields = [
	  'tag_name',
	  ]

	list_display = [
	  'tag_name',
	  'company',
	  'active_status',
	  'created_at', 
	  ]

	actions = [make_active, make_deactive]
	list_display_links = None
	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return False

	def has_add_permission(self, request, obj=None):
		return True

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			obj.updated_at = datetime.now()
		obj.save()

class KotStepsAdmin(admin.ModelAdmin):
	exclude = [
		'active_status',
		'created_at',
		'updated_at',
	  ]

	list_filter = [
		'Company__company_name',
		'active_status',
		'created_at',
		'updated_at',
		]

	search_fields = [
	  'product__product_name',
	  ]

	list_display = [
	  'Company',
	  'product',
	  'variant',
	  'kot_category',
	  'step_name',
	  'kot_desc',
	  'active_status',
	  ]

	actions = [make_active, make_deactive]
	# list_display_links = None
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


class ProductApiLogAdmin(admin.ModelAdmin):
	exclude = [
		# 'created_at'
	  ]

	list_filter = [
		'created_at',
		]

	search_fields = [
	  # 'product__product_name',
	  ]

	list_display = [
	  	'request_data',
		'response_data',
		'created_at',
	  ]

	readonly_fields = ['request_file', 'request_data', 'response_data']

	# actions = [make_active, make_deactive]
	# list_display_links = None
	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return True

	def has_add_permission(self, request, obj=None):
		return False

	# def save_model(self, request, obj, form, change):
	# 	if not change:
	# 		obj.created_at = datetime.now()
	# 	else:
	# 		obj.updated_at = datetime.now()
	# 	obj.save()



class CachedMenuDataAdmin(admin.ModelAdmin):
	exclude = [
		# 'created_at'
	  ]

	list_filter = [
		'outlet',
		'created_at',
		]

	search_fields = [
	  # 'product__product_name',
	  ]

	list_display = [
	  	'outlet',
		# 'response_data',
		'created_at',
	  ]

	readonly_fields = ['outlet', 'menu_data', 'created_at','updated_at']

	# actions = [make_active, make_deactive]
	# list_display_links = None
	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return True

	def has_add_permission(self, request, obj=None):
		return False

	# def save_model(self, request, obj, form, change):
	# 	if not change:
	# 		obj.created_at = datetime.now()
	# 	else:
	# 		obj.updated_at = datetime.now()
	# 	obj.save()

admin.site.register(ProductCategory,CategoryMasterAdmin)
admin.site.register(ProductsubCategory,SubCategoryMasterAdmin)
admin.site.register(Variant,VariantMasterAdmin)
admin.site.register(FoodType,FoodTypeMasterAdmin)
admin.site.register(AddonDetails,AddonDetailsMasterAdmin)
admin.site.register(Addons,AddonsMasterAdmin)
admin.site.register(Product,ProductMasterAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(KotSteps,KotStepsAdmin)
admin.site.register(ProductApiLog,ProductApiLogAdmin)

admin.site.register(CachedMenuData,CachedMenuDataAdmin)