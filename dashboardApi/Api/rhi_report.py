from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from django.db.models import Q
import calendar
from django.db.models import Sum

#Serializer for api
from rest_framework import serializers
from Product.models import ProductCategory, AddonDetails, Variant
from Orders.models import Order, OrderTracking, OrderProcessTimeLog

# from django.db.models import Count, Sum, Max, Avg, Case, When, Value, IntegerField, BooleanField
# from django.db.models.functions import ExtractYear, ExtractMonth,ExtractWeek, \
# ExtractWeekDay, Extract
from datetime import datetime, timedelta
from Brands.models import Company

from dashboardApi.Api.Validation.report_error_check import *
from rest_framework_tracking.mixins import LoggingMixin


def outlet_rhi_report(outlet_ids,order_record,order_process_log):
	response = []
	result = []
	for i in outlet_ids:
		data_dict =  {}
		order_q = order_record.filter(outlet=i)
		data_dict["outlet_id"] = i
		data_dict["outlet_name"] = OutletProfile.objects.filter(id=i)[0].Outletname
		all_order = order_q.count()
		data_dict['percent_rated_order'] = 0
		data_dict['ratings'] = 0
		data_dict['order_acceptance_time'] = 0
		data_dict['kpt'] = 0
		data_dict['kpt_to_dispatch'] = 0
		data_dict['ttk'] = 0
		data_dict['acceptance_percentage'] = 0
		data_dict['cancel_percent'] = 0
		if all_order == 0:
			pass
		else:
			rated_order = order_q.filter(~Q(rating=None)).count()
			if rated_order != 0:
				data_dict['percent_rated_order'] = \
				round(rated_order / all_order * 100,2)
				all_rating_sum = \
				round(order_q.aggregate(Sum('rating'))['rating__sum'],2)
				data_dict['ratings'] = \
				round(all_rating_sum / rated_order, 2)
			else:
				data_dict['percent_rated_order'] = 0
				data_dict['ratings'] = 0
			q = \
			order_process_log.filter(order__outlet=i)
			order_log_count = q.count()
			if order_log_count != 0:
				acceptance_time = \
				q.aggregate(Sum('order_acceptance_time'))['order_acceptance_time__sum']
				data_dict['order_acceptance_time'] = \
				round(acceptance_time/order_log_count,2)
				kpt_sum = q.aggregate(Sum('kpt'))['kpt__sum']
				data_dict['kpt'] = \
				round(kpt_sum/order_log_count,2)
				kpt_to_dispatch__sum = \
				q.aggregate(Sum('kpt_to_dispatch'))['kpt_to_dispatch__sum']
				data_dict['kpt_to_dispatch'] = \
				round(kpt_to_dispatch__sum/order_log_count,2)
				ttk__sum = q.aggregate(Sum('ttk'))['ttk__sum']
				data_dict['ttk'] = \
				round(data_dict['order_acceptance_time'] + data_dict['kpt'] + \
				data_dict['kpt_to_dispatch'],2)
			else:
				pass
			accepted_orders = order_q.filter(~Q(order_status=1)).count()
			cancel_orders = order_q.filter(order_status=7).count()
			data_dict['acceptance_percentage'] = \
			round(accepted_orders / all_order * 100,2)
			data_dict['cancel_percent'] = \
			round(cancel_orders / all_order * 100,2)
		result.append(data_dict)

	overall_result = []
	overall_data_dict = {}
	overall_data_dict["outlet_name"] = "Total"
	overall_data_dict['percent_rated_order'] = 0
	overall_data_dict['ratings'] = 0
	overall_data_dict['order_acceptance_time'] = 0
	overall_data_dict['kpt'] = 0
	overall_data_dict['kpt_to_dispatch'] = 0
	overall_data_dict['ttk'] = 0
	overall_data_dict['acceptance_percentage'] = 0
	overall_data_dict['cancel_percent'] = 0
	order_record = order_record.filter(outlet__in=outlet_ids)
	all_order = order_record.count()
	if all_order != 0:
		overall_data_dict['percent_rated_order'] = \
		rated_order = order_record.filter(~Q(rating=None)).count()
		if rated_order != 0:
			overall_data_dict['percent_rated_order'] = \
			round(rated_order / all_order * 100,2)
			all_rating_sum = \
			round(order_record.aggregate(Sum('rating'))['rating__sum'],2)
			overall_data_dict['ratings'] = \
			round(all_rating_sum / rated_order, 2)
		else:
			overall_data_dict['percent_rated_order'] = 0
			overall_data_dict['ratings'] = 0
		q = \
		order_process_log.filter(order__outlet__in=outlet_ids)
		all_order_log_count = q.count()
		if all_order_log_count != 0:
			overall_acceptance_time = \
			q.aggregate(Sum('order_acceptance_time'))['order_acceptance_time__sum']
			overall_data_dict['order_acceptance_time'] = \
			round(overall_acceptance_time/all_order_log_count,2)
			overall_kpt_sum = q.aggregate(Sum('kpt'))['kpt__sum']
			overall_data_dict['kpt'] = \
			round(overall_kpt_sum/all_order_log_count,2)
			overall_kpt_to_dispatch__sum = \
			q.aggregate(Sum('kpt_to_dispatch'))['kpt_to_dispatch__sum']
			overall_data_dict['kpt_to_dispatch'] = \
			round(overall_kpt_to_dispatch__sum/all_order_log_count,2)
			overall_ttk__sum = q.aggregate(Sum('ttk'))['ttk__sum']
			overall_data_dict['ttk'] = \
			round(overall_data_dict['order_acceptance_time'] + overall_data_dict['kpt'] + \
			overall_data_dict['kpt_to_dispatch'],2)
		else:
			pass
		accepted_orders = order_record.filter(~Q(order_status=1)).count()
		cancel_orders = order_record.filter(order_status=7).count()
		overall_data_dict['acceptance_percentage'] = \
		round(accepted_orders / all_order * 100,2)
		overall_data_dict['cancel_percent'] = \
		round(cancel_orders / all_order * 100,2)
	else:
		pass
	overall_result.append(overall_data_dict)
	response.append(result)
	response.append(overall_result)
	return response

class dashboardRHI(LoggingMixin,APIView):
	"""
	RHI Report Dashboard retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of RHI Report Dashboard data.

		Data Post: {
			"start_date"		   : 	"2020-06-02",
			"end_date"			   : 	"2020-06-03",
			"outlet_ids"	   	   : 	["18","40"]
		}

		Response: {

			"success"	: 	True, 
			"message"	: 	"RHI Report Dashboard data anaysis api worked well!!",
			"data"		: 	final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			user = request.user.id
			validation_check = err_check(data)
			if validation_check != None:
				return Response(validation_check)
			integrity_check = record_integrity_check(data,user)
			if integrity_check != None:
				return Response(integrity_check) 
			start_date = dateutil.parser.parse(data["start_date"]).date()
			end_date = dateutil.parser.parse(data["end_date"]).date()	
			order_record = Order.objects.filter(order_time__date__gte=start_date,\
												order_time__date__lte=end_date)
			order_process_log = \
			OrderProcessTimeLog.objects.filter(order__order_time__date__gte=start_date,\
											order__order_time__date__lte=end_date)
			if order_record.count() == 0:
				return Response(
				{
					"success": True,
 					"message": "No orders found!!"
				}
				)
			else:
				all_result = outlet_rhi_report(data["outlet_ids"],order_record,order_process_log)
				result = all_result[0]
				overall_result = all_result[1]
				return Response({
							"success"		: 	True, 
							"message"		: 	"RHI Report Dashboard data anaysis api worked well!!",
							"data" 			: 	result,
							"overall_data"	:	overall_result
							})
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})