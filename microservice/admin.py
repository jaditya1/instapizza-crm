# from django.contrib import admin
# from microservice.models import Microservice
# from datetime import datetime
# from django.contrib.admin import site
# from django.forms.utils import ErrorList
# from django import forms
# from django.contrib.auth.models import User
# from Configuration.admin import make_active, make_deactive
# from Configuration.models import PaymentDetails,ColorSetting,DeliverySetting, AnalyticsSetting



# def user_create(username, password):
# 	user_creation = User.objects.create_user(
# 						username=username,
# 						password=password,
# 						is_staff=False,
# 						is_active=True
# 						)
# 	return user_creation

# class MicroserviceAdmin(admin.ModelAdmin):
# 	exclude = [
# 			'created_at',
# 			'updated_at',
# 			'auth_user',
# 			'active_status'
# 			]
# 	search_fields = [

# 		]
# 	list_display = [
# 		  'company',
# 		  'username',
# 		  'active_status',
# 		  'created_at',
# 		  'updated_at',
# 			]

# 	actions = [make_active, make_deactive]

# 	list_per_page = 10

# 	def save_model(self, request, obj, form, change):
# 		if not change:
# 			created = user_create(obj.username, obj.password)
# 			user_id = User.objects.get(id=created.id)
# 			obj.auth_user = user_id
# 			obj.save()
# 		else:
# 			auth_user = User.objects.filter(id = obj.auth_user_id)
# 			auth_user.update(username=obj.username)
# 			for user in auth_user:
# 				user.set_password(obj.password)
# 				user.save()
# 			obj.updated_at = datetime.now()
# 			obj.save()

# 	def has_delete_permission(self, request, obj=None):
# 		return False

# 	def has_add_permission(self, request, obj=None):
# 		return True

# admin.site.register(Microservice,MicroserviceAdmin)

