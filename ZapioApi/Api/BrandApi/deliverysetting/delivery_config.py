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
from UserRole.models import ManagerProfile
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user


class DeliveryConfig(APIView):
	
	"""
	Delivery & Packaging Config GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for delivery & Packaging charge Configuration details.

	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			from Brands.models import Company
			user = self.request.user.id
			auth_id = user
			Company_id = get_user(auth_id)
			record = DeliverySetting.objects.filter(company=Company_id)
			if record.count() > 0:
				return Response({
							"success"   : True, 
							"delivery_charge" 	: record[0].delivery_charge,
							"package_charge"	: record[0].package_charge,
							"id"	: record[0].id,
							"active_status" : record[0].active_status,
							"symbol" : record[0].symbol,
							"SGST" : record[0].tax_percent,
							"CGST" : record[0].CGST
 							})
			else:
				err_message = {}
				err_message["settings"] = "Please contact to super-admin to set parameters for this!!"
				return Response({
							"success": False, 
							"error" :  err_message
							})
		except Exception as e:
			print("Delivery Charge Configuration retrieval Api Stucked into exception!!")
			print(e)
			return Response({
							"success": False, 
							"message": "Error happened!!", 
							"errors": str(e)})