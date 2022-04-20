from django.contrib import admin
from Brands.models import Company
from datetime import datetime
from UserRole.models import *
from django.contrib.admin import site
from django.forms.utils import ErrorList
from django import forms
from django.contrib.auth.models import User
from Configuration.admin import make_active, make_deactive


def admin_with_default(modeladmin, request, queryset):
	for q in queryset:
		user_type = UserType.objects.filter(Company=1,user_type=q.user_type.user_type)
		default_id = user_type[0].id
		update_q = ManagerProfile.objects.filter(id=q.id).update(user_type=default_id)
admin_with_default.short_description = "Change User Type to Default"


class UserTypeMasterAdmin(admin.ModelAdmin):
	# form = CompanyForm
	exclude = [
			'created_at',
			'updated_at',
			'active_status'
			]
	search_fields = [
		'user_type',
		]
	list_display = [
		  'user_type',
		  'Company',
		  'active_status',
		  'created_at',
			]
	list_filter = [
		'active_status',
		'created_at',
		'updated_at',
		'Company__company_name'
		]
	actions = [make_active, make_deactive]
	list_per_page = 10
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


class ManagerProfileMasterAdmin(admin.ModelAdmin):
	# form = CompanyForm
	exclude = [
			'auth_user',
			'created_at',
			'updated_at',
			'active_status'
			]
	search_fields = [
		'username',
		'manager_name'
		]
	list_display = [
		  'user_type',
		  'manager_name',
		  'manager_picture',
		  'Company',
		  'active_status',
		  'created_at',
			]
	list_filter = [
		'active_status',
		'created_at',
		'updated_at',
		'Company__company_name'
		]
	actions = [make_active, make_deactive, admin_with_default]
	list_per_page = 10
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
		return False

class MainRoutingModuleMasterAdmin(admin.ModelAdmin):
	# form = CompanyForm
	exclude = [
			'created_at',
			'updated_at',
			'active_status'
			]
	search_fields = [
		'module_id',
		'module_name'
		]
	list_display = [
		  'module_id',
		  'module_name',
		  'icon',
		  'label',
		  'to',
		  'active_status',
		  'created_at',
			]
	list_filter = [
		'active_status',
		'created_at',
		'updated_at'
		]
	actions = [make_active, make_deactive]
	list_per_page = 10
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

class RoutingModuleMasterAdmin(admin.ModelAdmin):
	# form = CompanyForm
	exclude = [
			'created_at',
			'updated_at',
			'active_status'
			]
	search_fields = [
	'module_name',
		]
	list_display = [
		  'main_route',
		  'module_name',
		  'icon',
		  'label',
		  'to',
		  'active_status',
		  'created_at',
			]
	list_filter = [
		'active_status',
		'created_at',
		'updated_at'
		]
	actions = [make_active, make_deactive]
	list_per_page = 10
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

class SubRoutingModuleMasterAdmin(admin.ModelAdmin):
	# form = CompanyForm
	exclude = [
			'created_at',
			'updated_at',
			'active_status'
			]
	search_fields = [
		'module_name'
		]
	list_display = [
		  'route',
		  'sub_module_name',
		  'icon',
		  'label',
		  'to',
		  'active_status',
		  'created_at',
			]
	list_filter = [
		'active_status',
		'created_at',
		'updated_at'
		]
	actions = [make_active, make_deactive]
	list_per_page = 10
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

class UserTypeAuthMasterAdmin(admin.ModelAdmin):
	# form = CompanyForm
	exclude = [
			'created_at',
			'updated_at',
			'active_status'
			]
	search_fields = [
		]
	list_display = [
		  'UserType',
		  # 'main_route',
		  # 'route',
		  # 'subroute',
		  'active_status',
		  'created_at',
			]
	list_filter = [
		'active_status',
		'created_at',
		'updated_at'
		]
	actions = [make_active, make_deactive]
	list_per_page = 10
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


admin.site.register(UserType,UserTypeMasterAdmin)
admin.site.register(ManagerProfile,ManagerProfileMasterAdmin)
admin.site.register(MainRoutingModule,MainRoutingModuleMasterAdmin)
admin.site.register(RoutingModule,RoutingModuleMasterAdmin)
admin.site.register(SubRoutingModule,SubRoutingModuleMasterAdmin)
admin.site.register(UserTypeAuthorization,UserTypeAuthMasterAdmin)



#  Billing Routing Module
class BillingMainRoutingModuleAdmin(admin.ModelAdmin):
	# form = CompanyForm
	exclude = [
			'created_at',
			'updated_at',
			'active_status'
			]
	search_fields = [
		'module_id',
		'module_name'
		]
	list_display = [
		  'module_id',
		  'module_name',
		  'icon',
		  'label',
		  'to',
		  'active_status',
		  'created_at',
			]
	list_filter = [
		'active_status',
		'created_at',
		'updated_at'
		]
	actions = [make_active, make_deactive]
	list_per_page = 10
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

class BillingRoutingModuleAdmin(admin.ModelAdmin):
	# form = CompanyForm
	exclude = [
			'created_at',
			'updated_at',
			'active_status'
			]
	search_fields = [
	'module_name',
		]
	list_display = [
		  'main_route',
		  'module_name',
		  'icon',
		  'label',
		  'to',
		  'active_status',
		  'created_at',
			]
	list_filter = [
		'active_status',
		'created_at',
		'updated_at'
		]
	actions = [make_active, make_deactive]
	list_per_page = 10
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

class BillingSubRoutingModuleAdmin(admin.ModelAdmin):
	# form = CompanyForm
	exclude = [
			'created_at',
			'updated_at',
			'active_status'
			]
	search_fields = [
		'module_name'
		]
	list_display = [
		  'route',
		  'sub_module_name',
		  'icon',
		  'label',
		  'to',
		  'active_status',
		  'created_at',
			]
	list_filter = [
		'active_status',
		'created_at',
		'updated_at'
		]
	actions = [make_active, make_deactive]
	list_per_page = 10
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
admin.site.register(BillingMainRoutingModule,BillingMainRoutingModuleAdmin)
admin.site.register(BillingRoutingModule,BillingRoutingModuleAdmin)
admin.site.register(BillingSubRoutingModule,BillingSubRoutingModuleAdmin)



# Roll Permission
class RollPermissionAdmin(admin.ModelAdmin):
	# form = CompanyForm
	exclude = [
			'created_at',
			'updated_at',
			'active_status'
			]
	search_fields = [
		# 'module_name'
		]
	list_display = [
		  'user_type',
		  'main_route',
		  'company',
		  'label',
		  'active_status',
		  'created_at',
			]
	list_filter = [
		'active_status',
		'created_at',
		'updated_at',
		'company',
		]
	actions = [make_active, make_deactive]
	list_per_page = 10
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


admin.site.register(RollPermission,RollPermissionAdmin)
admin.site.register(BillRollPermission,RollPermissionAdmin)