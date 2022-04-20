import requests
from Orders.models import Order, OrderProcessTimeLog
from Brands.models import Company
from UserRole.models import ManagerProfile
from dashboardApi.Api.order_report import outlet_order_report
from dashboardApi.Api.rhi_report import outlet_rhi_report
from datetime import datetime,timedelta
import json
import random
import time 
import dateutil.parser
from Configuration.models import DailyMailReporter
from django.db import connections
from django.utils import timezone


secret_token = "83c1e2c6ab0cb1fded654cbb1662b350b4a058b11d38576c125925a1f0d00a1e"

def auto_email_send_module(toe,send_data,company_id,subject, type_mail):
	url = "https://jaditya.pythonanywhere.com/api/mailservice/insta/"
	# url = "http://192.168.43.18:8080/api/mailservice/insta/"
	data = {}
	data["mail_content"] = send_data
	data["primary_mail"] = toe
	data["subject"] = subject
	data["type"] = type_mail
	headers = {}
	headers["token"] = secret_token
	headers["Content-Type"] = "application/json"
	response = requests.request("POST", url, data=json.dumps(data), headers=headers)
	response_data = response.json()
	if response_data["success"] == True:
		is_delivered = True
	else:
		is_delivered = False
	return "mail_sent"

li1 = [25,35,65,45,15,75,85,50,60,40]


def automail_sales_report_mgr():
	# now = timezone.localtime(timezone.now())
	# hrs = now.hour
	# mins = now.minute
	record = ManagerProfile.objects.filter(active_status=1)
	company_id = record[0].Company_id
	now = datetime.now()
	today = str(now.date())
	time_24_hours_ago = now - timedelta(days=1)
	last_date = str(time_24_hours_ago.date())
	last_date = dateutil.parser.parse(last_date)
	today = dateutil.parser.parse(today)
	try:
		for q in record:
			if q.email == None:
				pass
			else:
				mail_type = "outlet_report"
				try:
					to = q.email
					outlet_ids = q.outlet
					orderdata = Order.objects.filter(order_time__gte=last_date,\
										order_time__lte=today)
					if outlet_ids != None and len(outlet_ids) != 0:
						all_result = outlet_order_report(outlet_ids,orderdata)
						result = all_result[0]
						overall_result = all_result[1]
						send_data = {}
						send_data["result"] = result
						send_data["overall_result"] = overall_result
						subject = "Daily Sales Report-"+str(last_date)
						auto_email_send_module(to,send_data,company_id,subject, mail_type)
						random.shuffle(li1)
						time.sleep(li1[0])
						report_create = \
						DailyMailReporter.objects.create(is_success=True, \
										mail_response="Mail sending was successful!!",\
										mail_type=mail_type,email=to)
					else:
						pass
				except Exception as e:
					report_create = \
					DailyMailReporter.objects.create(is_success=False, mail_response=str(e),\
										mail_type=mail_type,email=to)
		close_all = connections.close_all()	
	except Exception as e:
		report_create = \
		DailyMailReporter.objects.create(is_success=False, mail_response=str(e),mail_type=mail_type)
	return "done"


def automail_rhi_report_mgr():
	# now = timezone.localtime(timezone.now())
	# hrs = now.hour
	# mins = now.minute
	record = ManagerProfile.objects.filter(active_status=1)
	company_id = record[0].Company_id
	now = datetime.now()
	today = str(now.date())
	time_24_hours_ago = now - timedelta(days=1)
	last_date = str(time_24_hours_ago.date())
	last_date = dateutil.parser.parse(last_date)
	today = dateutil.parser.parse(today)
	try:
		for q in record:
			if q.email == None:
				pass
			else:
				try:
					to = q.email
					outlet_ids = q.outlet
					orderdata = Order.objects.filter(order_time__gte=last_date,\
										order_time__lte=today)
					if outlet_ids != None and len(outlet_ids) != 0:
						order_process_log = \
						OrderProcessTimeLog.objects.filter(order__order_time__gte=time_24_hours_ago)
						all_result = outlet_rhi_report(outlet_ids,orderdata, order_process_log)
						result = all_result[0]
						overall_result = all_result[1]
						send_data = {}
						send_data["result"] = result
						send_data["overall_result"] = overall_result
						subject = "Daily RHI Report-"+str(last_date)
						mail_type = "rhi_report"
						auto_email_send_module(to,send_data,company_id,subject, mail_type)
						random.shuffle(li1)
						time.sleep(li1[0])
						report_create = \
						DailyMailReporter.objects.create(is_success=True, \
										mail_response="Mail sending was successful!!",\
										mail_type=mail_type,email=to)
					else:
						pass
				except Exception as e:
					report_create = \
					DailyMailReporter.objects.create(is_success=False, mail_response=str(e),\
										mail_type=mail_type,email=to)
		close_all = connections.close_all()	
	except Exception as e:
		report_create = \
		DailyMailReporter.objects.create(is_success=False, mail_response=str(e),mail_type=mail_type)
	return "done"