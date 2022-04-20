from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime

#Serializer for api
from rest_framework import serializers
from Product.models import ProductCategory
from discount.models import PercentOffers
from Outlet.models import DeliveryBoy,OutletProfile
from zapio.settings import Media_Path

class DeliveryBoyRetrieve(APIView):
	"""
	Delivery boy POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of delivery boy within brand.

		Data Post: {
			"id"                   : "3"
		}

		Response: {

			"success": True, 
			"message": "Delivery retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			data["id"] = str(data["id"])
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Category Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			delivery_record = DeliveryBoy.objects.filter(id=data['id'])
			if delivery_record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Delivery boy data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = delivery_record[0].id
				q_dict["name"] = delivery_record[0].name
				q_dict["email"] = delivery_record[0].email
				q_dict["mobile"] = delivery_record[0].mobile
				q_dict["address"] = delivery_record[0].address
				q_dict["active_status"] = delivery_record[0].active_status
				q_dict['outlet'] = []
				if len(delivery_record[0].outlet) > 0:
					a = delivery_record[0].outlet
					for i in a:
						out = {}
						out['label'] = OutletProfile.objects.filter(id=str(i))[0].Outletname
						out['key'] = str(i)
						out['value'] = str(i)
						q_dict['outlet'].append(out)
				else:
					pass

				domain_name = Media_Path
				if delivery_record[0].profile_pic != "" and delivery_record[0].profile_pic != None:
					full_path = domain_name + str(delivery_record[0].profile_pic)
					q_dict['profile_pic'] = full_path
				final_result.append(q_dict)

			return Response({
						"success": True, 
						"message": "Delivery boy retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Delivery boyretrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
