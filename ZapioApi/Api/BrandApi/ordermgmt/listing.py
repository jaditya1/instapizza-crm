from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Orders.models import Order,OrderStatusType, OrderTracking
from Outlet.models import DeliveryBoy,OutletProfile
from django.db.models import Q
from datetime import datetime, timedelta
import math  
import dateutil.parser
from ZapioApi.api_packages import *
from django.db.models import Sum
from rest_framework_tracking.mixins import LoggingMixin



class OrderListingData(LoggingMixin,APIView):
	"""
	Order listing and searching  POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for Order listng and searcing of Brand.

		Data Post: {
			"start_date"            : "2019-07-24 00:00:00:00",
			"end_date"              : "2019-07-29 00:00:00:00"  
			"outlet_id"             : []                    
		}

		Response: {

			"status"			:	True,
			"orderdata"			:	result,
			"pending_orders" 	: 	pending_orders,
			"cancelled"      	: 	cancel_orders,
			"gmv"		     	: 	overall_subtotal,
			"netsale"        	: 	overall_net_sales,
			"grosssale"      	:	overal_gross,
			"totaltax"       	: 	overall_taxes,
			"totaldis"       	: 	overall_discount_value,
			"totalorder"     	: 	total_settle_order
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			data = request.data
			err_message = {}
			s_date = data['start_date']
			e_date = data['end_date']
			try:
				start_date = dateutil.parser.parse(s_date)
				end_date = dateutil.parser.parse(e_date)
				if start_date < end_date:
					pass
				else:
					err_message["date"] = "Please provide meaning full date range!!"
			except Exception as e:
				err_message["date"] = "Please provide meaning full date range!!"
			if len(data["outlet_id"]) == 0:
				err_message["outlet"] = "Please select at least one outlet!!"
			else:
				for i in data["outlet_id"]:
					try:
						i = int(i)
					except Exception as e:
						err_message["outlet"] = "Outlet is not valid!!"
						break
			if any(err_message.values())==True:
					return Response({
						"success"	: 	False,
						"error" 	: 	err_message,
						"message" 	: 	"Please correct listed errors!!"
						})
			outlet = data['outlet_id']
			order_record = Order.objects.filter(order_time__gte=start_date,\
												order_time__lte=end_date, \
												outlet__in=data["outlet_id"])
			settle_order = order_record.filter(order_status = 6)
			cancel_orders = order_record.filter(order_status = 7)
			pending_orders = order_record.filter(Q(order_status = 1) | Q(order_status = 2) |
						Q(order_status = 3) | Q(order_status = 4) | Q(order_status = 5))

			result = []
			for i in order_record:
				p_list ={}
				p_list["id"] = i.id
				p_list["order_id"] = i.outlet_order_id
				p_list['order_source'] = i.order_source
				if i.payment_mode != None:
					p_list['payment_mode'] = i.get_payment_mode_display()
				else:
					p_list['payment_mode'] = "N/A"
				p_list['outlet_name'] = i.outlet.Outletname
				order_status_rec = OrderStatusType.objects.filter(id=i.order_status_id)
				if order_status_rec.count() != 0:
					p_list['order_status_name'] =\
					order_status_rec.first().Order_staus_name
					p_list['color_code'] = order_status_rec.first().color_code
				else:
					return Response(
						{"message":"Order Status Configuration data is not set in backend!!"})
				o_time = i.order_time+timedelta(hours=5,minutes=30)
				p_list['order_time'] = o_time.strftime("%d/%b/%y %I:%M %p")
				result.append(p_list)
			overall_settle_q = settle_order.filter(outlet__in=outlet)
			total_settle_order = overall_settle_q.count()
			total_cancel_orders = cancel_orders.count()
			if total_settle_order != 0:
				overall_subtotal = \
				round(overall_settle_q.aggregate(Sum('sub_total'))['sub_total__sum'],2)
				overall_external_discount = \
				overall_settle_q.aggregate(Sum('external_discount'))['external_discount__sum']\
				 or 0
				overall_discount_value = \
				round(overall_settle_q.aggregate(Sum('discount_value'))['discount_value__sum'],2)
				overall_discount_value = \
				round((overall_discount_value - overall_external_discount),2)
				overall_net_sales = \
				round((overall_subtotal - overall_discount_value),2)
				overall_taxes = \
				round(overall_settle_q.aggregate(Sum('taxes'))['taxes__sum'],2)
				overal_gross = \
				round(overall_net_sales + overall_taxes,2)
			else:
				overall_subtotal = 0
				overall_external_discount = 0
				overall_discount_value = 0
				overall_net_sales = 0
				overall_taxes = 0
				overal_gross = 0
			return Response({
						"status"			:	True,
						"orderdata"			:	result,
						"pending_orders" 	: 	pending_orders.count(),
						"cancelled"      	: 	total_cancel_orders,
						"gmv"		     	: 	overall_subtotal,
						"netsale"        	: 	overall_net_sales,
						"grosssale"      	:	overal_gross,
						"totaltax"       	: 	overall_taxes,
						"totaldis"       	: 	overall_discount_value,
						"totalorder"     	: 	total_settle_order
						})
		except Exception as e:
			return Response({
					"error"		:	str(e)
					})





