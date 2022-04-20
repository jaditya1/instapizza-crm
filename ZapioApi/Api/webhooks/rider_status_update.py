from rest_framework.views import APIView
from rest_framework.response import Response
import json
from datetime import datetime
from pos.models import POSOrder
from datetime import datetime, timedelta
from urbanpiper.models import OutletSync, RiderStatusRawApiResponse, UrbanOrders, RiderStatusLog
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework import serializers
from Orders.models import Order,OrderTracking
import random
import time
from _thread import start_new_thread
import math

li1 = [3.2,3.8,3.45,4.2,3.35,3,3.11]

def rider_status_manager(data):
	start = time.time()*1000
	random.shuffle(li1)
	time.sleep(li1[0])
	response = {}
	try:
		order_id = str(data["order_id"])
		order_status = data["delivery_info"]["current_state"]
		rider_detail = {}
		rider_detail["name"] = data["delivery_info"]["delivery_person_details"]["name"]
		rider_detail["email"] = "N/A"
		rider_detail["mobile"] =  data["delivery_info"]["delivery_person_details"]["phone"]
		urban_order = UrbanOrders.objects.filter(order_id=order_id)
		if urban_order.count() == 0:
			response={
				"success" : False,
				"message" : "Order is not valid!!"
				}
			end = time.time()*1000
			time_taken = math.ceil((end-start))
			log_create = \
			RiderStatusLog.objects.create(request_data=data,response_data=response,run_time=time_taken)
			return None
		else:
			pass
		outlet_id = urban_order[0].outlet_id
		outlet_check = OutletSync.objects.filter(outlet=outlet_id,sync_status="synced")
		if outlet_check.count() == 0:
			response={
				"success" : False,
				"message" : "Outlet is not valid!!"
				}
			end = time.time()*1000
			time_taken = math.ceil((end-start))
			log_create = \
			RiderStatusLog.objects.create(request_data=data,response_data=response,run_time=time_taken)
			return None
		else:
			pass
		company_id = outlet_check[0].company_id
		sync_outlet_id = outlet_check[0].id
		raw_record_create = \
		RiderStatusRawApiResponse.objects.create(company_id=company_id,sync_outlet_id=sync_outlet_id,\
			api_response=data)
		order_data = Order.objects.filter(urban_order_id=order_id)
		order_data_update = order_data.update(delivery_boy_details=rider_detail,is_rider_assign=1)
		response = {
			"success" 	:	True,
			"message"	:	"Rider status updated succesfully!!"

		}
		end = time.time()*1000
		time_taken = math.ceil((end-start))
		log_create = \
		RiderStatusLog.objects.create(request_data=data,response_data=response,run_time=time_taken)
		return None
	except Exception as e:
		end = time.time()*1000
		time_taken = math.ceil((end-start))
		response["message"] = "Some Exception happened: "+str(e)+"!!"
		response["success"] = False
		log_create = \
		RiderStatusLog.objects.create(request_data=data,response_data=response,run_time=time_taken)
		return None





class RiderStatusUpdate(LoggingMixin, APIView):
	"""
	Rider Status Update Hook POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for handling webhook mechanism for rider status update in urbanpiper.

	"""
	def post(self, request, format=None):
		try:
			data = request.data
			start_new_thread(rider_status_manager, (data,))
			return Response({
						"success": True, 
						"message": "Rider Staus Update webhook mechanism api worked well!!"
						})
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
