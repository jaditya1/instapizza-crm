from datetime import datetime
import json
from django.db.models import Sum, Q
from rest_framework import serializers
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from Dunzo.models import Unprocessed_Order_Quote, Processed_Order_Quote, \
						Order_Task, Task_State_Updates, Client_details
from Orders.models import Order, OrderStatusType, OrderTracking
from Outlet.models import OutletProfile
from Dunzo.Api.validation.order_address_validate import validate_address, validate_address_update, \
	validate_customer_details, validate_customer_details_update
from rest_framework_tracking.mixins import LoggingMixin
from frontApi.order.error_radious_check import check_circle


class Quote_Serializer(serializers.ModelSerializer):
	class Meta:
		model = Processed_Order_Quote
		fields = "__all__"


class Task_Serializer(serializers.ModelSerializer):
	class Meta:
		model = Order_Task
		fields = "__all__"



def OrderTask(data):
	import string
	import random
	a = random.choices(string.ascii_lowercase +
					   string.digits, k=8) + ['-'] + random.choices(string.ascii_lowercase +
														string.digits, k=4) + ['-'] + random.choices(
			string.ascii_lowercase +
			string.digits, k=4) + ['-'] + random.choices(string.ascii_lowercase +
														 string.digits, k=4) + ['-'] + random.choices(
			string.ascii_lowercase +
			string.digits, k=12)
	request_id=''.join(a)  # request_id for task
	try:
		user = data["user"]
		order_id = Order.objects.filter(id=data['order_id'])
		quote_id = Processed_Order_Quote.objects.filter(order_quote_id = order_id[0])
		if quote_id.count() != 0: # it will count whether the qoute is prepared for order or not
			pass
		else:
			return Response({
					"success"			: 	False,
					"message"			: 	"no quote exits!!"
				})
		order_task_id = Order_Task.objects.filter(order_id = order_id[0]) # if task is created for this order
																			# it will return the data
		if order_task_id.count() == 0:
			pass
		else:
			serializer = Task_Serializer(order_task_id, many=True)
			return Response({
						"success": True,
						"data": serializer.data,
						"message": "Task was already created for this order!!"
					})
		client = Client_details.objects.all()
		headers = {}
		headers["client-id"] = client[0].client_id
		headers["Authorization"] = client[0].client_token
		# headers["test"] = "true"
		# headers["Authorization"] = request.headers['Authorization']
		headers["Content-Type"] = "application/json"
		# url = 'https://apis-staging.dunzo.in/api/v1/tasks'
		url = 'https://api.dunzo.in/api/v1/tasks'
		import requests
		if order_id[0].special_instructions == None or order_id[0].special_instructions == '':
			special_instructions = "no special instructions"
		else:
			special_instructions = order_id[0].special_instructions
		if order_id[0].outlet.mobile_with_isd == None or order_id[0].outlet.mobile_with_isd == '':
			mobile_with_isd = '8882052000'
		else:
			mobile_with_isd = order_id[0].outlet.mobile_with_isd
		body = {
				"request_id": request_id,
				"pickup_details": {
				# "lat": 12.9468154,
				"lat": float(order_id[0].outlet.latitude),
				# "lng": 77.6472151,
				"lng": float(order_id[0].outlet.longitude),
				"address": {
				"apartment_address" : str(order_id[0].outlet.address),
				"street_address_1": str(order_id[0].outlet.address),
				"street_address_2": str(order_id[0].outlet.address),
				"landmark": str(order_id[0].outlet.address),
				"city": str(order_id[0].outlet.address),
				"state": str(order_id[0].outlet.address),
				"pincode": str(order_id[0].outlet.pincode),
				"country": "India"
				}
				},
				"drop_details": {
				"lat": float(order_id[0].address['latitude']),
				# "lat": 12.9468354,
				"lng": float(order_id[0].address['longitude']),
				# "lng": 77.6474151,
				"address": {
				"apartment_address" : str(order_id[0].address['address']),
				"street_address_1": str(order_id[0].address['address']),
				"street_address _2": str(order_id[0].address['address']),
				"landmark": str(order_id[0].address['landmark']),
				"city": str(order_id[0].address['city']),
				"state": str(order_id[0].address['state']),
				"pincode": str(order_id[0].address['pincode']),
				"country": "India"
				}
			},
			"sender_details": {
			"name": order_id[0].outlet.username,
			"phone_number": mobile_with_isd
			},

			"receiver_details": {
			"name": order_id[0].customer['name'],
			"phone_number": str(order_id[0].customer['mobile_number'])
			},
			"package_content": ["Food | Flowers"],
			"special_instructions": special_instructions
		}
		PARAMS = {}
		PARAMS["test"] = True
		r = requests.post(url,headers=headers, data=json.dumps(body))
		q = r.json()
		if r.status_code == 201:
			task_data = Order_Task(order_id = order_id[0],task_id=q['task_id'],request_id = request_id,state=q['state'],
								   estimated_price = q['estimated_price'],eta = q['eta'])
			task_data.save()
			return Response({
					"success"   :   True,
					"status"    :   r.status_code,
					"message"   : 	"Task is created successfully for this order!!"
				})
		elif r.status_code == 500:
			return Response({
					"success": True,
					"status": r.status_code,
					"message": str(q),
				})
		else:
			return Response({
					"success": False,
					"status": r.status_code,
					"message": str(q)
				})

	except Exception as e:
		return Response({
			"success"	: 	False, 
			"message"	: 	"Error happened!!", "errors": str(e)
			})

class GetQuote(LoggingMixin,APIView):

	"""
	Getting Quote for order POST API

		Authentication Required     :   Yes
		Service Usage & Description :   This service is used for getting quote of any order from dunzo.

		Data Post: {
			
			"order_id"      :   "1234"

		}

		Response: {

			"success"   :   True,
			"status"    :   r.status_code,
			"data"      :   q,
			"message"   :   "Quote is recieved successfully!!"
		}

	"""

	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			user = request.user.id
			order_id = Order.objects.filter(id=data['order_id'])
			if order_id.count() != 0:   # count the order is there or not
				pass
			else:
				return Response(
				{
					"success"			: 	False,
					"message"			: 	"no order id exits!!"
				}
				)
			order_address = order_id[0]
			if order_address.order_type != "Delivery" and order_address.order_type != "":
				return Response(
				{
					"success"			: 	False,
					"message"			: 	"Order type is not delivery!!"
				}
				)
			else:
				pass
			response = validate_address(order_address)  # validate the address present in order
			if response == None:
				pass
			else:
				return response
			order_customer = order_id[0]
			response = validate_customer_details(order_customer) # validate the customer details like phone and name
			if response == None:
				pass
			else:
				return response
			if order_id[0].is_aggregator == True: # payment_mode should not be swiggy or zomato
				return Response(
					{
						"success"			: 	False,
						"message"			: 	"This order cannot be processed with dunzo!!"
					}
				)
			else:
				pass
			if order_id[0].order_status.id > 3:  #.order status should be food ready maximum(3).
				return Response(
					{
						"success"			: 	False,
						"message"			: 	"It is already dispatched!!"
					}
				)
			else:
				pass
			q = Processed_Order_Quote.objects.filter(order_quote_id = order_id[0]) # it will check the qoute is alraedy is there or not for this order
							
			is_quoted = 0
			if q.count() == 0:
				pass
			else:
				serializer = Quote_Serializer(q, many=True)
				is_quoted = 1
				# return Response(
				# 	{
				# 		"success": True,
				# 		"data": serializer.data,
				# 		"message": "It is already quoted!!"
				# 	}
				# )

			if is_quoted == 0:
				outlet_id = order_id[0].outlet_id
				distance_check = {}
				distance_check["shop_id"] = outlet_id
				distance_check["lat"] = order_id[0].address['latitude']
				distance_check["long"] = order_id[0].address['longitude']

				service_check = check_circle(distance_check)
				if service_check == None:
					pass
				else:
					return Response(service_check)

				client = Client_details.objects.all()
				headers = {}
				headers["client-id"] = str(client[0].client_id)
				headers["Authorization"] = str(client[0].client_token)
				headers["Content-Type"] = "application/json"
				# url = 'https://apis-staging.dunzo.in/api/v1/quote?'
				url = 'https://api.dunzo.in/api/v1/quote?'
				# 12.9468154,
				# "lat": float(order_id[0].outlet.latitude),
				# "lng": 77.6872151
				payload = {
							'pickup_lat': order_id[0].outlet.latitude,
							'pickup_lng': order_id[0].outlet.longitude,
							# 'pickup_lat': '12.9468154',
							# 'pickup_lng': '77.6872151',
							'drop_lat': order_id[0].address['latitude'],
							'drop_lng': order_id[0].address['longitude'],
							# 'drop_lat': '12.9468154',
							# 'drop_lng': '77.6472151',
							'category_id': "pickup_drop"
				}
				import requests
				r = requests.get(url,headers=headers,params=payload)
				q = r.json()
				try:
					un_qoute_data = Unprocessed_Order_Quote(order_quote_id=order_id[0], raw_api_response=q)
					un_qoute_data.save()
					qoute_data = \
					Processed_Order_Quote(order_quote_id=order_id[0],category_id=q['category_id'],\
														distance=q['distance'],
													   estimated_price=q['estimated_price'],
													   eta = q['eta'])
					qoute_data.save()
				except Exception:
					return Response(
						{
							"success": False,
							"data": q
						}
					)
				if r.status_code == 200:
					order_data = {}
					order_data["order_id"] = data['order_id']
					order_data["user"] = request.user.id
					create_order_task = OrderTask(order_data)
					return create_order_task
				else:
					return Response({
							"success"	: 	False,
							"status"	: 	r.status_code,
							"data"		: 	q
						})
			else:
				order_data = {}
				order_data["order_id"] = data['order_id']
				order_data["user"] = request.user.id
				create_order_task = OrderTask(order_data)
				return create_order_task
		except Exception as e:
			return Response({
				"success"	: 	False, 
				"message"	: 	"Error happened!!", "errors": str(e)
				})




class OrderAddressCustomerUpdate(LoggingMixin,APIView):

	"""
	Address or Customer detail update POST API

		Authentication Required     :   Yes
		Service Usage & Description :   Service is used to update customer or address or both details of any order for dunzo.
		Instructions                :   "address" and "customer" both keys are optional means if you provide "address" key then address will be updated and if "customer" key is there that will be updated and if both are there both will be updated.

		Data Post: {
			
			"order_id"      :   "1234",
			"address"       :   {
								"city"          :   "Noida",
								"state"         :   "UP",
								"latitude"      :   "2.456897",
								"longitude"     :   "2.466689",
								"landmark"      :   "Teen murti",
								"pincode"       :   "4589632"
	
								}
			"customer"      :   {
								"name"              :   "Aditya",
								"mobile_number"     :   "9999999999"
								}
		}

		Response: {

			"success"   :   True,
			"message"   :   "Successfully updated details!!"
		}

	"""

	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			order_id = Order.objects.filter(id=data['order_id'])
			if 'address' in data: # it will update and validate the address of customer
				response = validate_address_update(data)
				if response == None:
					if order_id.count() != 0:
						for i in order_id:
							i.address = data['address']
							i.save()
					else:
						return Response(
							{
								"success": False,
								"message": "No order id exits!!"
							}
						)
				else:
					return response
					
			if 'customer' in data: #it will update and validate the name and number of customer
				response = validate_customer_details_update(data)
				if response == None:
					if order_id.count() != 0:
						for i in order_id:
							i.customer['name'] = data['customer']['name']
							i.customer['mobile_number'] = data['customer']['mobile_number']
							i.save()
					else:
						return Response(
							{
								"success": False,
								"message": "No order id exits!!"
							}
						)
				else:
					return response
			return Response(
				{
					"success": True,
					"message": "Successfully updated details!!"
				}
			)

		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})









class OrderTaskStatus(LoggingMixin,APIView):

	"""
	Getting order status update POST API

		Authentication Required     :   Yes
		Service Usage & Description :   This service is used for getting order status update from dunzo.

		Data Post: {
			
			"order_id"      :   "1234"

		}

		Response: {

			"success"   :   True,
			"status"    :   r.status_code,
			"data"      :   q,
		}

	"""

	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			user = request.user.id
			order_id = Order_Task.objects.filter(order_id__id = data['order_id'])
			if order_id.count() != 0: # it will check the task is created or not if created it will show the status
										# for this order
				pass
			else:
				return Response(
				{
					"success"			: 	False,
					"message"			: 	"No task_id exits!!"
				}
				)
			client = Client_details.objects.all()
			headers = {}
			headers["client-id"] = str(client[0].client_id)
			headers["Authorization"] = str(client[0].client_token)
			headers["Content-Type"] = "application/json"
			# url = 'https://apis-staging.dunzo.in/api/v1/tasks/'+'{'+order_id[0].task_id+'}' +'/status'
			url = 'https://api.dunzo.in/api/v1/tasks/'+'{'+order_id[0].task_id+'}' +'/status'
			import requests
			r = requests.get(url,headers=headers)
			q = r.json()
			if r.status_code == 200:
				for i in order_id:
					i.state = q['state']
					i.save()

				return Response(
					{
						"success": True,
						"status" : r.status_code,
						"data" : q,
					}
				)
			elif r.status_code == 500:
				return Response(
					{
						"success": True,
						"status": r.status_code,
						"data": q,
					}
				)
			else:
				return Response(
					{
						"success": False,
						"status": r.status_code,
						"data": q
					}
				)

		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})

def update_order_delivery_boy_details(data):


	order_task_id = Order_Task.objects.filter(task_id=data['task_id'])
	if order_task_id.count() != 0:

		order_id = Order.objects.filter(order_id=order_task_id[0].order_id)
		if order_id.count() != 0:
			delivery_boy_details = {}
			delivery_boy_details["name"] = data['runner']['name']
			delivery_boy_details["email"] = "N/A"
			delivery_boy_details["mobile"] = data['runner']['phone_number']
			record_update = order_id.update(delivery_boy_details=delivery_boy_details)
			return None
		else:
			return Response(
				{
					"success": False,
					"message": "please check your order id"
				})
	else:
		return Response(
			{
				"success": False,
				"message": "please check your task id"
			})


def update_order_order_status(data):
	order_task_id = Order_Task.objects.filter(task_id=data['task_id'])
	if order_task_id.count() != 0:
		order_row_id = order_task_id[0].order_id_id
		order_id = Order.objects.filter(id=order_row_id)
		if order_id.count() != 0:
			if data['state'] == "pickup_complete":
				if order_id[0].order_status_id < 4:
					order_state = OrderStatusType.objects.get(priority=4)
					for i in order_id:
						i.order_status = order_state
						i.save()
						order_trac = OrderTracking.objects.filter(Q(order = order_id[0]),Q(Order_staus_name__priority = 4))
						if order_trac.count() == 0:
							order_t= OrderTracking(order = order_id[0],Order_staus_name = order_state,created_at = datetime.now())
							order_t.save()
							return None
						else:
							for i in order_trac:
								i.updated_at = datetime.now()
								i.save()
							return None
				else:
					return Response(
						{
							"success": False,
							"message": "This order is already dispatched!!"
						})
			else:
				pass
			if data['state'] == "delivered":
				if order_id[0].order_status.id == 4:
					for i in order_id:
						order_state = OrderStatusType.objects.get(priority = 5)
						i.order_status = order_state
						i.delivery_time = datetime.now()
						i.save()
						order_track = OrderTracking.objects.filter(Q(order=order_id[0]),Q(Order_staus_name__priority = 5))
						if order_track.count() == 0:
							order_t = OrderTracking(order=order_id[0], Order_staus_name=order_state,created_at = datetime.now())
							order_t.save()
							return None
						else:
							for i in order_track:
								i.updated_at = datetime.now()
								i.save()
							return None
				else:
					return Response(
						{
							"success": False,
							"message": "This order is already delivered!!"
						})
			else:
				return None
		else:
			return Response(
				{
					"success": False,
					"message": "please check your order id"
				})
	else:
		return Response(
			{
				"success": False,
				"message": "please check your task id"
			})


#webhook
class WebhookTaskStateUpdate(LoggingMixin,APIView):

	"""
	Webhhok order status update POST API

		Authentication Required     :   Yes
		Service Usage & Description :   This service is used for receiving order status update from dunzo 
										through webhook mechanism.

	"""

	def post(self, request, format=None):
		data = request.data
		try:
			created_at = datetime.now()
			if "reference_id" in data:
				ref_id = data["reference_id"]
			else:
				ref_id = None
			if data['state'] in ['queued', 'runner_cancelled']:
				updatedata = Task_State_Updates(
					event_type= data['event_type'],
					event_id = data['event_id'],
					task_id = data['task_id'],
					reference_id = ref_id,
					state = data['state'],
					created_at = created_at,
					# event_timestamp = event_time,
					eta = data['eta'],
					# request_timestamp = request_time
					)
				updatedata.save()
				return Response(
					{
						"success"	: 	True,
						"message"	: 	"successfully" +' '+ data['state'] +' '+"by Dunzo"
					})
			if data['state'] in ['runner_accepted', 'reached_for_pickup']:
				response = update_order_delivery_boy_details(data)
				if response == None:
					pass
				else:
					return response
				updatedata = Task_State_Updates(
						event_type=data['event_type'],
						event_id=data['event_id'],
						task_id=data['task_id'],
						reference_id=ref_id,
						state=data['state'],
						created_at = created_at,
						# event_timestamp=event_time,
						eta=data['eta'],
						runner=data['runner'],
						# request_timestamp=request_time
					)
				updatedata.save()
				return Response(
					{
						"success": True,
						"message": "successfully" +' '+ data['state'] +' '+ "by Dunzo"
					})

			if data['state'] in ['pickup_complete', 'started_for_delivery', 'reached_for_delivery']:
				if data['state'] == "pickup_complete":
					response = update_order_order_status(data)
					if response == None:
						pass
					else:
						return response
				else:
					pass
				response = update_order_delivery_boy_details(data)
				if response == None:
					pass
				else:
					return response
				updatedata = Task_State_Updates(
					event_type= data['event_type'],
					event_id = data['event_id'],
					task_id = data['task_id'],
					reference_id = ref_id,
					state = data['state'],
					created_at = created_at,
					eta = data['eta'],
					runner=data['runner']
					)
				updatedata.save()
				return Response(
					{
						"success": True,
						"message": "successfully" +' '+ data['state'] +' '+ "by Dunzo"
					})

			if data['state'] =='delivered':
				response = update_order_order_status(data)
				if response == None:
					pass
				else:
					return response
				updatedata = Task_State_Updates(
					event_type= data['event_type'],
					event_id = data['event_id'],
					task_id = data['task_id'],
					reference_id = ref_id,
					state = data['state'],
					created_at = created_at,
					price = data['price']
					)
				updatedata.save()
				return Response(
					{
						"success": True,
						"message": "successfully" +' '+ data['state'] +' '+ "by Dunzo"
					})

			if data['state'] == 'cancelled':
				updatedata = Task_State_Updates(
					event_type= data['event_type'],
					event_id = data['event_id'],
					task_id = data['task_id'],
					reference_id = ref_id,
					state = data['state'],
					created_at = created_at,
					cancelled_by = data['cancelled_by'],
					cancellation_reason = data['cancellation_reason'],
					)
				updatedata.save()
				return Response(
					{
						"success": True,
						"message": "successfully" +' '+ data['state'] +' '+ "by Dunzo!!"
					})
			else:
				return Response(
					{
						"success"	: 	False,
						"message"	: 	"you cannot update the order!!"
					})
		except Exception as e:
			return Response(
				{
					"success": False,
					"message": str(e)
				})


#For future implementation
#Manual Order Cancellation
class CancelOrderTask(APIView):

	def post(self, request, format=None):
		try:
			data = request.data
			user = request.user.id
			order_id = Order_Task.objects.filter(order_id__id = data['order_id'])

			s =  ["runner_accepted","reached_for_pickup","created","queued"]

			if order_id.count() != 0:
				if order_id[0].task_id != "" or order_id[0].task_id != None:
					if order_id[0].state in s:
						pass
					else:
						return Response(
							{
								"success"		: 	False,
								"message"			: 	"you cannot cancel the order after pickup completed!!"
							})
				else:
					return Response(
						{
							"success"		: 	False,
							"message"			: 	"No task_id exits to cancel the order!!"
						}
					)
			else:
				return Response(
				{
					"success"			: 	False,
					"message"			: 	"No task_id exits to cancel the order!!"
				}
				)
			body = {
				"cancellation_reason" : "Changed my mind"
			}
			client = Client_details.objects.all()
			headers = {}
			headers["client-id"] = client[0].client_id
			headers["Authorization"] = client[0].client_token
			headers["Content-Type"] = "application/json"
			url = 'https://apis-staging.dunzo.in/api/v1/tasks/'+'{'+order_id[0].task_id+'}' +'/_cancel'
			import requests
			r = requests.post(url,headers=headers,data=json.dumps(body))
			if r.status_code == 204:
				for i in order_id:
					i.state = "cancelled"
					i.save()
				return Response(
					{
						"success": True,
						"status" : r.status_code,
						"data" : 'q',
					}
				)
			else:
				return Response(
					{
						"success": False,
						"status": r.status_code,
					}
				)

		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
