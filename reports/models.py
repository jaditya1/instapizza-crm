from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import ArrayField,JSONField

class Report(models.Model):
	auth_id = models.ForeignKey(User, related_name='user_report', on_delete=models.CASCADE
								  , verbose_name='User id')
	report_name = models.CharField(max_length=200, null=True, blank=True, verbose_name='Report Name')
	report = models.FileField(upload_to ='xls_reports/', null=True, blank=True, verbose_name='Report')
	file_size = models.FloatField(max_length=200, null=True, blank=True, verbose_name='Report Size')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')

	class Meta:
			verbose_name = 'User Reports'
			verbose_name_plural = 'User Reports'

	def __str__(self):
			if self.report_name:
					return self.report_name


class ReportErrorGenerator(models.Model):
	error_report = \
	JSONField(blank=True,null=True, verbose_name="Error in report generation")
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')


	class Meta:
		verbose_name = "   Error Reports"
		verbose_name_plural = "   Error Reports"

	def __str__(self):
		return str(self.error_report)


