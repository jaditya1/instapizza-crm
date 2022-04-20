from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime, timedelta
from django.db.models import Q

#Serializer for api
from rest_framework import serializers
from Product.models import ProductCategory, AddonDetails, Variant
from Orders.models import Order,OrderStatusType




class TrackOrder(APIView):
	"""
	Order Track by mobile number or by order id

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to track order by mobile nubmer or by order id.

		Data Post: {
			"mobile"		   : "8750477098",
		}

		Response: {

			"success": True, 
			"orderdata":ord_data
		}

	"""
	# permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			# outlet_id = OutletProfile.objects.filter(auth_user=request.user.id).first().id
			data = request.data
			err_message ={}
			err_message["mobile"] = \
						validation_master_anything(data["mobile"],
						"Mobile or Order ID",vat_re, 3)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			mdata = data['mobile']
			track_data = Order.objects.filter(Q(customer__mobile_number=mdata) | Q(order_id=mdata)).order_by('-order_time')
			if track_data.count()!=0:
				i = track_data[0]
				# track_datas = track_data.filter(order=i.id)
				ord_data =[]
				p_list ={}
				add = i.address
				p_list['id'] = i.id
				p_list['order_id'] = i.order_id
				p_list['longitude'] = add['longitude']
				p_list['latitude'] = add['latitude']
				p_list['address'] = add['address']
				p_list['locality'] = add['locality']
				p_list['city'] = add['city']
				p_list['order_status'] = i.order_status_id
				t = i.order_time+timedelta(hours=5,minutes=30)
				p_list['order_time'] = t.strftime("%d/%b/%y %I:%M %p")
				if  i.payment_mode == '0':
					p_list['payment_mode'] = "Cash on Delivery"
				else:
					p_list['payment_mode'] = "Online"
				p_list['order_status_name'] = i.order_status.Order_staus_name
				# p_list['color_code'] = OrderStatusType.objects.filter(id=i.order_status_id).first().color_code
				cus = i.customer
				p_list['name'] = cus['name']
				p_list['mobile_number'] = cus['mobile_number']
				p_list['email'] = cus['email']
				p_list['order_description'] = i.order_description
				ord_data.append(p_list)
			return Response({"status":True,
							"orderdata":ord_data
							})
		except Exception as e:
			print("Track Order Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})

