from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
from rest_framework import serializers
from Configuration.models import DeliverySetting
from ZapioApi.Api.BrandApi.deliverysetting.serializer import DeliverySerializer
from django.db.models import Q
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

class DeliveryEdit(APIView):

	"""
	Delivery & Packaging Configuration Edit POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to edit the delivery & packaging Configuration details.

		Data Post: {
		    "delivery_charge"                : "#ffd600",
    		"package_charge"                   : "#000",
    		"tax_percent"                : "#ffd600",
    		"CGST"                   : "#000",
  			"id"                          : "1"
		}

		Response: {

			"success"  : True, 
			"message"  : "Theme api worked well!!",
			"data"     : final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			user = request.user
			auth_id = user.id
			Company_id = get_user(auth_id)
			err_message = {}
			err_message["delivery_charge"] =  \
							only_required(str(data["delivery_charge"]), "Delivery Charge")
			if err_message["delivery_charge"] == None:
				try:
					data["delivery_charge"] = float(data["delivery_charge"])
				except Exception as e:
					err_message["delivery_charge"] =\
					"Please provide valid delivery charges!!"
			else:
				pass
			err_message["package_charge"] =  \
							only_required(str(data["package_charge"]), "Packaging Charge")
			if err_message["package_charge"] == None:
				try:
					data["package_charge"] = float(data["package_charge"])
				except Exception as e:
					err_message["package_charge"] =\
					"Please provide valid packaging charges!!"
			else:
				pass
			err_message["symbol"] = validation_master_anything(data["symbol"],
								"Currency",alpha_re, 1)
			err_message["tax_percent"] = validation_master_anything(str(data["tax_percent"]),
								"Tax Percentage",lat_long_re, 1)
			err_message["CGST"] = validation_master_anything(str(data["CGST"]),
								"CGST Percentage",lat_long_re, 1)

			if err_message["tax_percent"] == None:
				if float(data["tax_percent"]) > 99:
					err_message["tax_percent"] = "Tax Percentage is not valid!!"
				else:
					pass
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			data["delivery_charge"] = float(data["delivery_charge"])
			data["package_charge"] = float(data["package_charge"])
			data["tax_percent"] = float(data["tax_percent"])
			data["CGST"] = float(data["CGST"])
			record = DeliverySetting.objects.filter(Q(id=data['id']),Q(company=Company_id))
			if record.count() == 0:
				return Response(
					{
						"status": False,
	 					"message": "Delivery Charge Configuration data is not valid to update!!"
					})
			else:
				data["updated_at"] = datetime.now()
				theme_serializer = \
					DeliverySerializer(record[0],data=data,partial=True)
				if theme_serializer.is_valid():
					data_info = theme_serializer.save()
					return Response({
						"status": True, 
						"message": "Delivery & Taxes Configuration is updated successfully!!",
						"data": theme_serializer.data
						})
				else:
					print("something went wrong!!")
					return Response({
						"status": False, 
						"message": str(theme_serializer.errors),
						})
		except Exception as e:
			print("Delivery Configuration retrieval Api Stucked into exception!!")
			print(e)
			return Response({
							"status": False, 
							"message": "Error happened!!", 
							"errors": str(e)})