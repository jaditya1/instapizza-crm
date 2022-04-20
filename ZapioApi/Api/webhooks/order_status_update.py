from rest_framework.views import APIView
from rest_framework.response import Response
import json
from django.db.models import Q
from pos.models import POSOrder
from datetime import datetime, timedelta
from urbanpiper.models import OutletSync, OrderStatusRawApiResponse, UrbanOrders,OrderStatusLog
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework import serializers
from Orders.models import Order
from datetime import datetime, timedelta
from Orders.models import Order,OrderStatusType,OrderTracking
import time
from _thread import start_new_thread
import math
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
import random

li = ["Acknowledged", "Food Ready", "Dispatched", "Completed", "Cancelled"]

li1 = [2.2,2.8,2.45,3.2,2.35,2,2.11]

def order_status_manager(data):
	start = time.time()*1000
	random.shuffle(li1)
	time.sleep(li1[0])
	response = {}
	try:
		urban_order_id = data["order_id"]
		order_id = str(data["order_id"])
		aggre_order_status = data["new_state"]
		urban_order = UrbanOrders.objects.filter(Q(order_state=aggre_order_status),\
										Q(order_id=order_id))
		if urban_order.count() == 1:
			response = {
				"success" : False,
				"message" : "Order is processed already for "+aggre_order_status+" status!!"
				}
			end = time.time()*1000
			time_taken = math.ceil((end-start))
			log_create = \
			OrderStatusLog.objects.create(request_data=data,response_data=response,run_time=time_taken)
			return None
		else:
			pass
		if aggre_order_status != "Acknowledged" and aggre_order_status != "Food Ready" and\
			aggre_order_status != "Placed":
			pass
		else:
			response = {
				"success" : False,
				"message" : "Order is processed for '"+aggre_order_status+"' staus at POS level already !!"
				}
			end = time.time()*1000
			time_taken = math.ceil((end-start))
			log_create = \
			OrderStatusLog.objects.create(request_data=data,response_data=response,run_time=time_taken)
			return None
		urban_order = UrbanOrders.objects.filter(~Q(order_state__icontains="Complet"),\
										Q(order_id=order_id))
		if urban_order.count() == 0:
			response = {
				"success" : False,
				"message" : "Order is not valid or already completed!!"
				}
			end = time.time()*1000
			time_taken = math.ceil((end-start))
			log_create = \
			OrderStatusLog.objects.create(request_data=data,response_data=response,run_time=time_taken)
			return None
		else:
			pass
		outlet_id = urban_order[0].outlet_id
		outlet_check = OutletSync.objects.filter(outlet=outlet_id,sync_status="synced")
		# api_ref = APIReference.objects.filter(ref_id=reference_id)
		if outlet_check.count() == 0:
			response = {
				"success" : False,
				"message" : "Outlet is not valid!!"
				}
			end = time.time()*1000
			time_taken = math.ceil((end-start))
			log_create = \
			OrderStatusLog.objects.create(request_data=data,response_data=response,run_time=time_taken)
			return None
		else:
			pass
		if urban_order[0].order_state == "Completed":
			response = {
				"success" : False,
				"message" : "Already processed!!"
				}
			end = time.time()*1000
			time_taken = math.ceil((end-start))
			log_create = \
			OrderStatusLog.objects.create(request_data=data,response_data=response,run_time=time_taken)
			return None
		else:
			pass
		company_id = outlet_check[0].company_id
		sync_outlet_id = outlet_check[0].id
		raw_record_create = \
		OrderStatusRawApiResponse.objects.create(company_id=company_id,
																sync_outlet_id=sync_outlet_id,\
																api_response=data)
		updated_at = datetime.now()
		status_update = urban_order.update(order_state=data["new_state"],updated_at=updated_at)
		main_order = Order.objects.filter(urban_order_id=order_id)
		main_order_id = main_order[0].id
		if aggre_order_status == "Dispatched":
			order_status_id = 4
		elif aggre_order_status == "Completed":
			order_status_id = 5
		elif aggre_order_status == "Cancelled":
			order_status_id = 7
		else:
			order_status_id = 1
		if order_status_id == 5:
			is_completed =  True
		else:
			is_completed = False
		if is_completed == True:
			is_paid = True
		else:
			is_paid = False
		if order_status_id == 5:
			delivery_time = updated_at
		else:
			delivery_time = None
		if main_order[0].order_status_id < 3 and order_status_id == 7:
			main_order_update = \
			main_order.update(Aggregator_order_status=aggre_order_status,is_completed=is_completed,
							is_paid=is_paid,delivery_time=delivery_time)
		else:
			main_order_update = \
			main_order.update(Aggregator_order_status=aggre_order_status, order_status=order_status_id,\
										is_completed=is_completed,is_paid=is_paid,\
									 delivery_time=delivery_time)
			order_track = \
			OrderTracking.objects.create(order_id=main_order_id, Order_staus_name_id=order_status_id)
		end = time.time()*1000
		time_taken = math.ceil((end-start))
		response = {
			"success" 	:	True,
			"message"	:	"Order status updated succesfully!!"

		}
		log_create = \
		OrderStatusLog.objects.create(request_data=data,response_data=response,run_time=time_taken)
		return None
	except Exception as e:
		end = time.time()*1000
		time_taken = math.ceil((end-start))
		response["message"] = "Some Exception happened: "+str(e)+"!!"
		response["success"] = False
		log_create = \
		OrderStatusLog.objects.create(request_data=data,response_data=response,run_time=time_taken)
		return None

class OrderStatusUpdate(LoggingMixin, APIView):
	"""
	Order Status Update Hook POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for handling webhook mechanism for order status update in urbanpiper.

	"""
	def post(self, request, format=None):
		data = request.data
		start_new_thread(order_status_manager, (data,))
		return Response({
					"success": True, 
					"message": "Order Staus Update webhook mechanism api worked well!!"
					})