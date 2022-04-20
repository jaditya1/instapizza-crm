from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
from rest_framework import serializers
from Configuration.models import ColorSetting
from UserRole.models import ManagerProfile
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user


class ThemeConfig(APIView):
	
	"""
	Theme Config GET API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for theme Configuration.

		Data Post: {
			
		}

		Response: {
			    "success": true,
			    "accent_color"     :     "rzp_live_xcgVtA1lIkJ",
			    "textColor"        :      "dgwbqAGqDcFXNRBYkXaP",
			    "secondaryColor"   :      "INR"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			from Brands.models import Company
			user = self.request.user.id
			Company_id = get_user(user)
			record = ColorSetting.objects.filter(company=Company_id)
			if record.count() > 0:
				return Response({
							"success"   : True, 
							"accent_color" 	: record[0].accent_color,
							"textColor"	: record[0].textColor,
							"secondaryColor"    : record[0].secondaryColor,
							"id"	: record[0].id,
							"active_status" : record[0].active_status
 							})
			else:
				return Response({
							"success": False, 
							"message": "No Data Found"
							})
		except Exception as e:
			print("Theme Configuration retrieval Api Stucked into exception!!")
			print(e)
			return Response({
							"success": False, 
							"message": "Error happened!!", 
							"errors": str(e)})