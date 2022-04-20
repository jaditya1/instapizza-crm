from datetime import datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from Customers.models import CustomerProfile
from zapio.settings import EMAIL_HOST_USER
from CustomerApi.serializers.notification_serializers import NotificationRecordSerializer
from Notification.models import NotificationConfiguration, NotificationRecord
from django.core.mail import EmailMessage


class EmailNotifications():
	def __init__(self, **notification_data):
		print(notification_data)
		self.status = False
		self.reason_for_failed = None
		self.customer = notification_data.get("customer_id", None)
		self.admin = 1 if notification_data.get("send_to_admin", None) else None
		self.notification_for = 'Admin' if self.admin else 'Customer'
		self.message_data = None
		self.message_body = None
		self.notification_type = None
		self.notification_category = "EMAIL"
		self.api_name = notification_data.get("api_name", None)
		self.otp = notification_data.get("otp", None)
		self.motp = notification_data.get("otp",None)
		self.current_datetime = datetime.now().strftime("%d %B %Y %I:%M %p")
		self.emailId = []
		self.email_html_template = notification_data.get("email_html_template", None)



	def notificationtype_from_apiname(self):
		api_dict = {
				"__registrationotpit__"    :  1,
		}
		self.notification_type = api_dict[self.api_name]

	def notification_msgbody_data(self):
		try:
			self.notificationtype_from_apiname()
			notification_instance = NotificationConfiguration.objects.filter(id=self.notification_type).first()
			if notification_instance:
				self.message_data = notification_instance.notification_type
				self.message_body = notification_instance.sample_content
				if self.message_body and self.notification_type == 1:
					self.message_body = str(self.message_body).replace("[CX-NAME]", str(self.name)) \
					   .replace("[XXXXX]", str(self.otp))
				else:
					self.message_body = str("Notification Type or Sample Content not Exist!")
			else:
				self.message_body = str("Notification Type not Exist!")
		except Exception as e:
			print("notification_msgbody_data-Exception")
			print(e)
			self.message_body = str("Notification-Type-not-Exist!")



	def email_send_module(self):
		try:
			subject = self.message_data
			from_email = EMAIL_HOST_USER
			to =  self.emailId
			html_content = render_to_string(self.email_html_template,{"message_data":self.message_body,
						})
			text_content = strip_tags(html_content)
			msg = EmailMultiAlternatives(subject, text_content, from_email, to, cc=[])
			msg.attach_alternative(html_content, "text/html")
			self.status = True if msg.send() else False
			self.reason_for_failed = "Email Service Not Configured" if not self.status else None
		except Exception as e:
			print(e)

	def notification_record_saved(self):
		notification_record = {
				"notification_category" : self.notification_category,
				"notification_type"     : self.notification_type,
				"user"                  : self.customer,
				"admin_user"            : self.admin,
				"notification_for"      : self.notification_for,
				"reason_for_failed"     : self.reason_for_failed,
				"status"                : self.status,
				"message_data"          : self.message_data,
				"massge_body"           : self.message_body,
				"otp"                   : self.otp,
				"motp"					: self.motp
		}
		notification_record_serializer = NotificationRecordSerializer(data=notification_record)
		if notification_record_serializer.is_valid():
			notification_record_serializer.save()
		else:
			print("@@ notification_record_serializer-Errors @@")
			print(notification_record_serializer.errors)


	def get_customer_details(self):
		customer_instance = CustomerProfile.objects.filter(id=self.customer).first()
		if customer_instance:
			self.name = customer_instance.name
			self.customermobileno = customer_instance.mobile
			self.customeremailid = customer_instance.email
			self.emailId.append(self.customeremailid)




	def main(self):
		if self.customer:
			self.get_customer_details()
		if self.admin:
			self.get_admin_emails()
		self.notification_msgbody_data()
		self.email_send_module()
		self.notification_record_saved()
	def __call__(self):
		self.main()


