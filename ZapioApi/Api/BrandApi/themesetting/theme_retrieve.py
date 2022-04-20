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


class ThemeRetrieve(APIView):
	"""
	Theme retrieval POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for retrieve the theme Configuration.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success"  : True, 
			"message"  : "Theme Configuration retrieval api worked well!!",
			"data"     : final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			record = ColorSetting.objects.filter(Q(id=data['id']),Q(company__auth_user=user.id))
			if record.count() == 0:
				return Response(
					{
						"status": False,
	 					"message": "Theme Configuration data is not valid to update!!"
					})
			else:
				theme_serializer = ThemeSerializer(record, many=True)
				return Response({
						"status": True, 
						"message": "Theme Configuration data updation api worked well!!",
						"data": theme_serializer.data
						})
		except Exception as e:
			print("Theme Configuration retrieval Api Stucked into exception!!")
			print(e)
			return Response({
							"status": False, 
							"message": "Error happened!!", 
							"errors": str(e)})