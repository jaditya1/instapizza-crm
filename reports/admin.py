from datetime import datetime

from django.contrib import admin

from reports.models import Report, ReportErrorGenerator


class UserReportAdmin(admin.ModelAdmin):
	exclude = ['auth_id']
	list_display=['auth_id','report_name','report','file_size','created_at']
	readonly_fields = ['report_name','report','file_size','created_at']

	def has_delete_permission(self, request, obj=None):
		return True

	def has_add_permission(self, request, obj=None):
		return False
	#
	#
	# def save_model(self, request, obj, form, change):
	#     if not change:
	#         obj.created_at = datetime.now()
	#     obj.save()

admin.site.register(Report, UserReportAdmin)


class ReportErrorGeneratorAdmin(admin.ModelAdmin):
	# exclude = ['auth_id']
	list_display=['error_report','created_at']
	readonly_fields = ['error_report','created_at']

	def has_delete_permission(self, request, obj=None):
		return True

	def has_add_permission(self, request, obj=None):
		return False
	#
	#
	# def save_model(self, request, obj, form, change):
	#     if not change:
	#         obj.created_at = datetime.now()
	#     obj.save()

admin.site.register(ReportErrorGenerator, ReportErrorGeneratorAdmin)

