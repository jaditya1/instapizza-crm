from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from ZapioApi.Api.BrandApi.profile.profile import CompanySerializer
import json
import requests
#Serializer for api
from rest_framework import serializers
from Orders.models import Order, OrderStatusType
from rest_framework.authtoken.models import Token
from Outlet.models import DeliveryBoy,OutletProfile
from django.db.models import Q
from datetime import datetime
from _thread import start_new_thread
import os
from zapio.settings import Media_Path, MEDIA_ROOT
import time
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user


class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = '__all__'

class orderNotificationCount(APIView):

	"""
	Order Notification Count Post API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for count for new Orders within Brand

	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		try:
			user = request.user.id
			cid = get_user(user)
			data = \
			Order.objects.filter(Q(Company=cid),Q(is_seen=0)).order_by('-order_time')
			ord_data =[]
			for i in data[:5]:
				p_list ={}
				add = i.address
				p_list['id'] = i.id
				p_list['order_id'] = i.order_id
				cus = i.customer
				if cus !='':
					if "email" in cus:
						p_list['email'] = cus['email']
					else:
						pass
					if "mobile_number" in cus:
						p_list['mobile'] = cus['mobile_number']

					if "mobile" in cus:
						p_list['mobile'] = cus['mobile']
					p_list['name'] = cus['name']
				else:
					pass
				ord_data.append(p_list)
			if data:
				countorders = data.count()
			else:
				countorders = 0
			result = []
			sound_path = Media_Path+"notification_sound.mp3"

			return Response({"status":True,
							"orderdetails" : ord_data,
							"ordercount": countorders,
							"sound" : sound_path
							 })
		except Exception as e:
			print(e)
			return Response({"status":False,
				             "message":ord_data,
				             "error" : str(e)
				             })


class orderNotificationAll(APIView):

	"""
	All Order Notification  Post API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for All Order within outlet

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			user = request.user.id
			cid = get_user(user)
			data = {}
			order_data = Order.objects.filter(Q(Company=cid))
			order_update = order_data.update(is_seen=1)
			orderdata = Order.objects.filter(Q(Company=cid),Q(is_seen=1)).order_by('-order_time')
			ord_data =[]
			for i in orderdata:
				p_list ={}
				add = i.address
				p_list['id'] = i.id
				p_list['order_id'] = i.order_id
				if add == None:
					pass
				else:
					if "longitude" in add:
						p_list['longitude'] = add['longitude']
					else:
						p_list['longitude'] = "N/A"
					if "latitude" in add:
						p_list['latitude'] = add['latitude']
					else:
						p_list['latitude'] = "N/A"
					if "address" in add:
						p_list['address'] = add['address']
					else:
						p_list['address'] = "N/A"
					if "locality" in add:
						p_list['locality'] = add['locality']
					else:
						p_list['locality'] = "N/A"

					if "city" in add:
						p_list['city'] = add['city']
					else:
						p_list['city'] = "N/A"

				p_list['order_status'] = i.order_status_id
				p_list['discount_value'] = i.discount_value
				p_list['sub_total'] = i.sub_total
				p_list['total_bill_value'] = i.total_bill_value
				p_list['order_time'] = i.order_time.strftime("%d/%b/%y %I:%M %p")
				if  i.payment_mode == '0':
					p_list['payment_mode'] = "Cash on Delivery"
				else:
					p_list['payment_mode'] = "Online"
				p_list['order_status_name'] = OrderStatusType.objects.filter(id=i.order_status_id).first().Order_staus_name
				p_list['color_code'] = OrderStatusType.objects.filter(id=i.order_status_id).first().color_code
				cus = i.customer
				if cus == None:
					pass
				else:
					p_list['name'] = cus['name']
					if "email" in cus:
						p_list['email'] = cus['email']
					else:
						pass
					if "mobile_number" in cus:
						p_list['mobile'] = cus['mobile_number']

					if "mobile" in cus:
						p_list['mobile'] = cus['mobile']
				p_list['order_description'] = i.order_description
				ord_data.append(p_list)
			return Response({"status":True,
							"orderdata":ord_data,
							})
		except Exception as e:
			print(e)



class orderNotificationSeen(APIView):

	"""
	Seen Notification All POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to Seen All order Notification..

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "Seen Updated Successfully",

		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			data = request.data
			order_record = Order.objects.filter(id=data['id'])
			if order_record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Order data is not valid to Seen!!"
				}
				)
			else:
				data["updated_at"] = datetime.now()
				data["is_seen"] = 1
				order_serializer = \
				OrderSerializer(order_record[0],data=data,partial=True)
				if order_serializer.is_valid():
					data_info = order_serializer.save()
					return Response(
					{
						"success": True,
	 					"message": "Seen Successfully"
					}
					)
				else:
					return Response(
					{
						"success": False,
	 					"message": order_serializer.errors
					}
					)
		except Exception as e:
			print(e)


