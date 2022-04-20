from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime

#Serializer for api
from rest_framework import serializers
from UserRole.models import UserType

class UserTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserType
		fields = '__all__'

class UserTypeAction(APIView):
	"""
	UserType Action POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to activate or deactivate UserType.

		Data Post: {
			"id"                   		: "2",
			"active_status"             : "0"
		}

		Response: {

			"success": True, 
			"message": "User Type is deactivated now!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			from django.db.models import Q
			data = request.data
			err_message = {}
			if data["active_status"] == "true":
				pass
			elif data["active_status"] == "false":
				pass
			else:
				err_message["active_status"] = "Active status data is not valid!!"
			err_message["id"] = \
						validation_master_anything(data["id"],
						"UserType Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = UserType.objects.filter(id=data["id"])
			if record.count() != 0:
				data["updated_at"] = datetime.now()
				if data["active_status"] == "true":
					info_msg = "User Type is activated successfully!!"
				else:
					info_msg = "User Type is deactivated successfully!!"
				serializer = \
				UserTypeSerializer(record[0],data=data,partial=True)
				if serializer.is_valid():
					data_info = serializer.save()
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(serializer.errors),
						})
			else:
				return Response(
					{
						"success": False,
						"message": "UserType id is not valid to update!!"
					}
					)
			return Response({
						"success": True, 
						"message": info_msg
						})
		except Exception as e:
			print("UserType action Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})