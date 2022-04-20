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
from ZapioApi.Api.BrandApi.themesetting.serializer import ThemeSerializer
from django.db.models import Q
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

class ThemeEdit(APIView):

	"""
	Theme Edit  POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for edit the theme Configuration.

		Data Post: {
		    "accent_color"                : "#ffd600",
    		"textColor"                   : "#000",
    		"secondaryColor"			  : "#ffa726"
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
			user = self.request.user.id
			Company_id = get_user(user)
			err_message = {}
			err_message["accent_color"] =  only_required(data["accent_color"],"Accent Color")
			err_message["textColor"] =  only_required(data["textColor"],"Text Color")
			err_message["secondaryColor"] =  only_required(data["secondaryColor"],"Secondary Color")
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})

			record = ColorSetting.objects.filter(Q(id=data['id']),Q(company=Company_id))
			if record.count() == 0:
				return Response(
					{
						"status": False,
	 					"message": "Theme Configuration data is not valid to update!!"
					})
			else:
				data["updated_at"] = datetime.now()
				theme_serializer = \
					ThemeSerializer(record[0],data=data,partial=True)
				if theme_serializer.is_valid():
					data_info = theme_serializer.save()
					return Response({
						"status": True, 
						"message": "Theme Configuration is updated successfully!!",
						"data": theme_serializer.data
						})
				else:
					print("something went wrong!!")
					return Response({
						"status": False, 
						"message": str(theme_serializer.errors),
						})
		except Exception as e:
			print("Theme Configuration retrieval Api Stucked into exception!!")
			print(e)
			return Response({
							"status": False, 
							"message": "Error happened!!", 
							"errors": str(e)})