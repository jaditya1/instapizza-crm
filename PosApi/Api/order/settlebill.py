from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from _thread import start_new_thread
from datetime import datetime
from django.db.models import Q
from Orders.models import Order, OrderStatusType, OrderTracking
import json
from Brands.models import Company
from discount.models import Coupon
from History.models import CouponUsed
from frontApi.serializer.customer_serializers import CustomerSignUpSerializer
from rest_framework_tracking.mixins import LoggingMixin

#Serializer for api
from rest_framework import serializers
import math
from Product.models import Product
from rest_framework.permissions import IsAuthenticated
from UserRole.models import ManagerProfile,UserType
from ZapioApi.api_packages import *
import requests 
from History.models import CouponUsed
from Outlet.models import OutletProfile,DeliveryBoy
from Location.models import *

class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = '__all__'

class RiderSerializer(serializers.ModelSerializer):
	class Meta:
		model = DeliveryBoy
		fields = '__all__'

class OrderBillSettle(LoggingMixin,APIView):
	"""
	Bill Settle  POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to Bill Settle


		Data Post:  {
		
			settlement_details:[
						{"mode":"0","amount":250},
						{"mode":"1","amount":150,"transaction_id":"razr_012365478uytre"}
						]
			"Payment_source":"paytm",
			"id"  : 4   
			
		}

		Response: {
				
				    "success": true,
				    "message": "Order Settled Updated successfully"
				
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			auth_user = request.user.id
			auth_record = ManagerProfile.objects.filter(auth_user=auth_user,active_status=1)
			if auth_record.count() == 0:
				return Response({
					"status"	:	False,
					"message"	:	"User not valid!!"
					})
			else:
				pass
			orderdata = {}
			orderdata["user"] = auth_record[0].manager_name
			err_message = {}
			rider = {}
			if "id" not in data:
				return Response({
						"success"	:	True,
						"message"	:	"Order ID not provided!!"
							})
			else:
				pass
			record = Order.objects.filter(id=str(data['id']),order_status=5)
			if  record.count() == 0:
				return Response({
						"success"	:	True,
						"message"	:	"Right now, order can'nt be settled!!"
							})
			else:
				pass

			if 'settlement_details' in data:
				sdetails = data["settlement_details"]
				if len(sdetails) > 0:
					for i in sdetails:
						if 'mode' in i and 'amount' in i:
							pass
						else:
							err_message["payment_detail"] = "Order mode and amount value is not set!!"
							break
						if i['mode'] != 0:
							if 'mode' in i and 'amount' in i and 'transaction_id' in i:
								orderdata['transaction_id'] = i['transaction_id']
							else:
								err_message["payment_detail"] = "Order mode and amount and transaction_id value is not set!!"
								break
						else:
							pass
						if i['mode'] == 0:
							orderdata['payment_mode'] = str(0)
						elif i['mode'] == 1:
							orderdata['payment_mode'] = str(1)
						elif i['mode'] == 2:
							orderdata['payment_mode'] = str(2)
						elif i['mode'] == 3:
							orderdata['payment_mode'] = str(3)
						elif i['mode'] == 4:
							orderdata['payment_mode'] = str(4)
						elif i['mode'] == 5:
							orderdata['payment_mode'] = str(5)
						elif i['mode'] == 6:
							orderdata['payment_mode'] = str(6)
						elif i['mode'] == 7:
							orderdata['payment_mode'] = str(7)
						elif i['mode'] == 8:
							orderdata['payment_mode'] = str(8)
						elif i['mode'] == 9:
							orderdata['payment_mode'] = str(9)
						elif i['mode'] == 10:
							orderdata['payment_mode'] = str(10)
						elif i['mode'] == 11:
							orderdata['payment_mode'] = str(11)
						elif i['mode'] == 12:
							orderdata['payment_mode'] = str(12)
						elif i['mode'] == 13:
							orderdata['payment_mode'] = str(13)
						elif i['mode'] == 14:
							orderdata['payment_mode'] = str(14)
						elif i['mode'] == 15:
							orderdata['payment_mode'] = str(15)
						elif i['mode'] == 16:
							orderdata['payment_mode'] = str(16)
						elif i['mode'] == 17:
							orderdata['payment_mode'] = str(17)
						else:
							pass
				else:
					pass
				if any(err_message.values())==True:
					return Response({
									"success": False,
									"error" : err_message,
									"message" : "Please correct listed errors!!"
								})
			else:
				pass
			if 'settlement_details' in data:
				if len(sdetails) > 1:
					orderdata['payment_mode'] = str(7)
				else:
					pass
			else:
				pass
			if record[0].is_aggregator == True:
				odata = []
				sd = []
				s = {}
				if record[0].aggregator_payment_mode =='COD':
					s['mode'] = 14
					s['amount'] = record[0].total_bill_value
					sd.append(s)
					orderdata['payment_mode'] = "14"
					orderdata["transaction_id"] = "COD"
				elif record[0].aggregator_payment_mode =='Swiggy':
					s['mode'] = 10
					s['amount'] = record[0].total_bill_value
					sd.append(s)
					orderdata['payment_mode'] = "10"
				else:
					s['mode'] = 15
					s['amount'] = record[0].total_bill_value
					orderdata['payment_mode'] = "15"
					sd.append(s)
				orderdata['settlement_details'] = sd
				orderdata['order_status'] = 6
				order_serializer = OrderSerializer(record[0],data=orderdata,partial=True)
				if order_serializer.is_valid():
					order_serializer.save()
					order_tracking = OrderTracking.objects.create(order_id=data['id'], 
					Order_staus_name_id=orderdata['order_status'], created_at=datetime.now())
					return Response({
							"success":True,
							"message":"Order settled successfully"
							})
				else:
					return Response({
							"success":False,
							"message":str(usedcoupon_serializer.errors)
							})	
			else:
				if "payment_mode" in orderdata:
					if orderdata['payment_mode'] == "0":
						orderdata["transaction_id"] = "COD"
					else:
						pass
				else:
					if record[0].aggregator_payment_mode =='COD':
						orderdata["transaction_id"] = "COD"
					else:
						pass
				if record[0].discount_name == "Complimentary":
					orderdata["transaction_id"] = "Complimentary"
				else:
					pass
				orderdata['settlement_details'] = data['settlement_details']
				orderdata['payment_source'] = data['Payment_source']
				orderdata['order_status'] = 6
				order_pre_data = record[0]
				order_serializer = OrderSerializer(record[0],data=orderdata,partial=True)
				if order_serializer.is_valid():
					order_serializer.save()
					order_tracking = OrderTracking.objects.create(order_id=data['id'], 
					Order_staus_name_id=orderdata['order_status'], created_at=datetime.now())
					if order_pre_data.is_rider_assign == True:
						alld = DeliveryBoy.objects.filter(id=record[0].delivery_boy_id)

						rider['is_assign'] = 0
						rider["updated_at"] = datetime.now()
						rider_serializer = RiderSerializer(alld[0],data=rider,partial=True)
						if rider_serializer.is_valid():
							rider_serializer.save()
							return Response({
								"success":True,
								"message":"Order settled successfully"
								})
					else:
						return Response({
								"success":True,
								"message":"Order settled successfully"
								})
				else:
					return Response({
							"success":False,
							"message":str(usedcoupon_serializer.errors)
							})	
		except Exception as e:
			print(e)
			return Response({"success": False,
							"message":"Order Settled api stucked into exception!!",
							"error" : str(e)})

