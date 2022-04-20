from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile, DeliveryBoy
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
import os
from django.db.models import Q
from OutletApi.Api.serializers.deliveryboy_serializers import DeliverySerializer
from rest_framework import serializers
from rest_framework.generics import ListAPIView
from Brands.models import Company
from Outlet.models import DeliveryBoy
from UserRole.models import ManagerProfile
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

class DeliveryBoyRegistration1(APIView):
	"""
	Delivery Boy Creation POST API
		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create new DeliveryBoy.
		Data Post: {
			"outlet"                       : [1,2],
			"name"			               : "umesh",
			"email"		                   : "umeshsamal3@gmail.com",
			"address" 					   : "sunlight colony ashram",
			"mobile" 	    			   : "8750477098",
			"profile_pic"                  : "a/jpg", (type:image)
		}
		Response: {
			"success": True,
			"message": "Delivery boy is registered successfully under your brand!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			err_message = {}
			data = request.data
			d = json.loads(data["outlet"])
			data['outlet'] = d
			user = request.user.id
			cid = get_user(user)
			data['Company'] = cid
			if "profile_pic" in data:
				pass
			else:
				data["profile_pic"] = None
			if len(data["outlet"]) != 0:
				outlet_unique_list = []
				for i in data["outlet"]:
					err_message["outlet_map"] = \
						validation_master_anything(str(i),
						"Outlet",contact_re, 1)
					if err_message["outlet_map"] != None:
						break
					if i not in outlet_unique_list:
						outlet_unique_list.append(i)
					else:
						err_message["duplicate_outlet"] = "Outlet are duplicate!!"
						break
					record_check = OutletProfile.objects.filter(Q(id=i),Q(active_status=1))
					if record_check.count() == 0:
						err_message["outlet"] = \
						"Outlet is not valid!!"
						break
			else:
				err_message["outlet"] = "Please Enter Outlet ID"
			
			err_message["name"] = \
					validation_master_anything(data["name"],
					"Name",username_re, 3)
			err_message["email"] = \
					validation_master_anything(data["email"],
					"Email",email_re, 3)
			err_message["address"] = \
					validation_master_anything(data["address"],
					"Address", address_re, 3)
			err_message["mobile"] = \
					validation_master_exact(data["mobile"], 
						"Mobile No.",contact_re, 10)
			if type(data["profile_pic"]) != str:
				im_name_path =  data["profile_pic"].file.name
				im_size = os.stat(im_name_path).st_size
				if im_size > 170*1024:
					err_message["image_size"] = "Profile Picture can'nt excced the size more than 170kb!!"
			else:
				data["profile_pic"] = None
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			data["active_status"] = 1
			if "id" in data:
				Delivery_record = DeliveryBoy.objects.filter(id=data['id'])
				if Delivery_record.count() == 0:
					return Response(
					{
						"success": False,
						"message": "Delivery Boy data is not valid to update!!"
					}
					)
				else:
					data["updated_at"] = datetime.now()
					update_data = \
					Delivery_record.update(outlet=d,\
					name=data["name"],email=data["email"],\
					mobile=data["mobile"],address=data["address"],\
					Company_id=data['Company'],
					updated_at=datetime.now())

					if data["profile_pic"] != None and data["profile_pic"] != "":
						product = DeliveryBoy.objects.get(id=data["id"])
						product.profile_pic = data["profile_pic"]
						product.save()
					else:
						pass
					if update_data:
						info_msg = "Delivery Boy is updated successfully!!"
					else:
						print("something went wrong!!")
						return Response({
							"success": False, 
							"message": str(serializer.errors),
							})

			else:
				p_query = \
					DeliveryBoy.objects.create(outlet=d,\
					name=data["name"],email=data["email"],\
					profile_pic=data["profile_pic"],mobile=data["mobile"],address=data["address"],\
					Company_id=data['Company'])
				if p_query:
					data_info=p_query
					info_msg = "Delivery Boy is created successfully!!"
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(serializer.errors),
						})
			return Response({
						"success": True, 
						"message": info_msg
						})
		except Exception as e:
				print(str(e))
				return Response({"success": False, 
								"message": "Error happened!!", 
								"errors": str(e)})
