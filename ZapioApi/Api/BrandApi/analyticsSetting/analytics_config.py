from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
from rest_framework import serializers
from Configuration.models import AnalyticsSetting
from UserRole.models import ManagerProfile
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user


class AnalyticsConfig(APIView):
	
	"""
	Analytics Config GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for Google analytics Configuration details.

	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			from Brands.models import Company
			auth_id = request.user.id
			Company_id = get_user(auth_id)
			record = AnalyticsSetting.objects.filter(company=Company_id)
			if record.count() > 0:
				return Response({
							"success"   : True, 
							"u_id" 	: record[0].u_id,
							"analytics_snippets"	: record[0].analytics_snippets,
							"id"	: record[0].id,
							"active_status" : record[0].active_status
 							})
			else:
				err_message = {}
				err_message["settings"] = "Please contact to super-admin to set parameters for this!!"
				return Response({
							"success": False, 
							"error" :  err_message
							})
		except Exception as e:
			print("Analytics Configuration retrieval Api Stucked into exception!!")
			print(e)
			return Response({
							"success": False, 
							"message": "Error happened!!", 
							"errors": str(e)})