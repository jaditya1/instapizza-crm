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
from UserRole.models import UserType


class UserTypeRetrieval(APIView):
	"""
	UserType retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of UserType data.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "UserType retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"UserType Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = UserType.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided UserType data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["user_type"] = record[0].user_type
				q_dict["active_status"] = record[0].active_status
				final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "UserType retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("UserType retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})