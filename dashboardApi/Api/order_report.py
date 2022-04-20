from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from django.db.models import Q
from django.db.models.functions import ExtractYear, ExtractMonth,ExtractWeek, ExtractWeekDay
from django.db.models.functions import Extract
import calendar
from Orders.models import Order

from django.db.models import Sum
from datetime import datetime, timedelta
from Brands.models import Company

from dashboardApi.Api.Validation.report_error_check import *
from rest_framework_tracking.mixins import LoggingMixin


def outlet_order_report(outlet_ids,order_record):
	response = []
	result = []
	for i in outlet_ids:
		q = order_record.filter(~Q(order_status=7),Q(outlet=i))
		data_dict = {}
		data_dict["outlet_id"] = i
		data_dict["outlet_name"] = OutletProfile.objects.filter(id=i)[0].Outletname
		data_dict["orders"] = q.count()
		for k in q:
			if k.total_items != None:
				pass
			else:
				total_items = len(k.order_description)
				q_update = q.filter(id=k.id).update(total_items=total_items)
		if q.count() == 0:
			data_dict['sub_total'] = 0
			data_dict['discount_value'] = 0
			data_dict['discount_percent'] = 0
			data_dict['net_sales'] = 0
			data_dict['taxes'] = 0
			data_dict['gross_sales'] = 0
			data_dict['aov'] = 0
			data_dict['item_per_order'] = 0
			data_dict['cancelled_order'] = 0
			data_dict['cov'] = 0
		else:
			data_dict['sub_total'] = \
			round(q.aggregate(Sum('sub_total'))['sub_total__sum'],2)
			external_discount = \
			q.aggregate(Sum('external_discount'))['external_discount__sum'] or 0
			data_dict['discount_value'] = \
			round(q.aggregate(Sum('discount_value'))['discount_value__sum'],2)
			data_dict['discount_value'] = \
			round((data_dict['discount_value'] - external_discount),2)
			data_dict['discount_percent'] = \
			round(data_dict['discount_value'] / data_dict['sub_total'] * 100,2)
			data_dict['net_sales'] = \
			round(data_dict['sub_total'] - data_dict['discount_value'],2)
			data_dict['taxes'] = \
			round(q.aggregate(Sum('taxes'))['taxes__sum'],2)
			data_dict['gross_sales'] = \
			round(data_dict['net_sales'] + data_dict['taxes'],2)
			data_dict['aov'] = round(data_dict['net_sales']/data_dict["orders"],2)
			total_items = q.aggregate(Sum('total_items'))['total_items__sum']
			data_dict['item_per_order'] = round(total_items/data_dict["orders"],2)
			#cancelled order analysis
			cancel_record = order_record.filter(Q(order_status=7),Q(outlet=i))
			data_dict['cancelled_order'] = cancel_record.count()
			if data_dict['cancelled_order'] == 0:
				data_dict['cov'] = 0
			else:
				cancel_sub_total = \
				round(cancel_record.aggregate(Sum('sub_total'))['sub_total__sum'],2)
				cancel_external_discount = \
				cancel_record.aggregate(Sum('external_discount'))['external_discount__sum'] or 0
				cancel_discount_value = \
				round(cancel_record.aggregate(Sum('discount_value'))\
					['discount_value__sum'],2)
				cancel_discount_value = \
				round((cancel_discount_value-cancel_external_discount),2)
				cancel_net_sales = cancel_sub_total - cancel_discount_value
				data_dict['cov'] = round(cancel_net_sales,2)

		result.append(data_dict)
	overall_result = []
	overall_data_dict = {}
	overall_data_dict["outlet_name"] = "Total"
	overall_record = order_record.filter(~Q(order_status=7))
	total_order_record = overall_record.filter(outlet__in=outlet_ids)
	if order_record.count() != 0:
		overall_data_dict['orders'] = total_order_record.count()
		overall_external_discount = \
		total_order_record.aggregate(Sum('external_discount'))['external_discount__sum'] or 0
		overall_data_dict['sub_total'] = \
		round(total_order_record.aggregate(Sum('sub_total'))['sub_total__sum'],2)
		overall_data_dict['discount_value'] = \
		round(total_order_record.aggregate(Sum('discount_value'))['discount_value__sum'],2)
		overall_data_dict['discount_value'] = \
		round((overall_data_dict['discount_value'] - overall_external_discount),2)
		overall_data_dict['discount_percent'] = \
		round(overall_data_dict['discount_value'] / overall_data_dict['sub_total'] * 100,2)
		overall_data_dict['net_sales'] = \
		round(overall_data_dict['sub_total'] - overall_data_dict['discount_value'],2)
		overall_data_dict['taxes'] = \
		round(total_order_record.aggregate(Sum('taxes'))['taxes__sum'],2)
		overall_data_dict['gross_sales'] = \
		round(overall_data_dict['net_sales'] + overall_data_dict['taxes'],2)
		overall_data_dict['aov'] = \
		round(overall_data_dict['net_sales']/overall_data_dict["orders"],2)
		overall_total_items = \
		total_order_record.aggregate(Sum('total_items'))['total_items__sum']
		overall_data_dict['item_per_order'] = \
		round(overall_total_items/overall_data_dict["orders"],2)

		#overall cancelled order analysis
		overall_cancel_record = order_record.filter(order_status=7,\
										outlet__in=outlet_ids)
		overall_data_dict['cancelled_order'] = overall_cancel_record.count()
		if overall_data_dict['cancelled_order'] == 0:
			overall_data_dict['cov'] = 0
		else:
			overall_cancel_sub_total = \
			overall_cancel_record.aggregate(Sum('sub_total'))['sub_total__sum']
			overall_cancel_external_discount = \
			overall_cancel_record.aggregate(Sum('external_discount'))['external_discount__sum']\
				or 0
			overall_cancel_discount_value = \
			overall_cancel_record.aggregate(Sum('discount_value'))['discount_value__sum']
			overall_cancel_discount_value = \
			round((overall_cancel_discount_value-overall_cancel_external_discount),2)
			overall_cancel_net_sales = \
			overall_cancel_sub_total - overall_cancel_discount_value
			overall_data_dict['cov'] = \
			round(overall_cancel_net_sales,2)
	else:
		overall_data_dict['orders'] = 0
		overall_data_dict['sub_total'] = 0
		overall_data_dict['discount_value'] = 0
		overall_data_dict['discount_percent'] = 0
		overall_data_dict['net_sales'] = 0
		overall_data_dict['taxes'] = 0
		overall_data_dict['gross_sales'] = 0
		overall_data_dict['aov'] = 0
		overall_data_dict['item_per_order'] = 0
		overall_data_dict['cancelled_order'] = 0
		overall_data_dict['cov'] = 0
	overall_result.append(overall_data_dict)
	response.append(result)
	response.append(overall_result)
	return response

class dashboardOrder(LoggingMixin,APIView):
	"""
	Order Report Dashboard retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Order Report Dashboard data.

		Data Post: {
			"start_date"		   : 	"2020-06-02",
			"end_date"			   : 	"2020-06-03",
			"outlet_ids"	   	   : 	["18","40"]
		}

		Response: {

			"success"	: 	True, 
			"message"	: 	"Order Report Dashboard data anaysis api worked well!!",
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
			if order_record.count() == 0:
				return Response(
				{
					"success": True,
 					"message": "No orders found!!"
				}
				)
			else:
				all_result = outlet_order_report(data["outlet_ids"],order_record)
				result = all_result[0]
				overall_result = all_result[1]
				return Response({
							"success"		: 	True, 
							"message"		: 	"Outlet Dashboard data anaysis api worked well!!",
							"data" 			: 	result,
							"overall_data"	:	overall_result
							})
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})