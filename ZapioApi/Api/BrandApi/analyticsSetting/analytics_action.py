from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
import os
from datetime import datetime

from django.db.models import Max

#Serializer for api
from rest_framework import serializers
from Configuration.models import AnalyticsSetting

class AnalyticsSerializer(serializers.ModelSerializer):
	class Meta:
		model = AnalyticsSetting
		fields = '__all__'

class AnalyticsAction(APIView):
	"""
	Analytics Action POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to activate or deactivate Analytics Configuration.

		Data Post: {
			"id"                   		: "2",
			"active_status"             : "0"
		}

		Response: {

			"success": True, 
			"message": "Analytics Configuration setting is deactivated successfully!!",
			"data": final_result
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
						"Theme Configuration Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = AnalyticsSetting.objects.filter(id=data["id"])
			if record.count() != 0:
				data["updated_at"] = datetime.now()
				if data["active_status"] == "true":
					info_msg = "Google Analytics Configuration setting is activated successfully!!"
				else:
					info_msg = "Google Analytics Configuration setting is deactivated successfully!!"
				serializer = \
				AnalyticsSerializer(record[0],data=data,partial=True)
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
						"message": "Analytics Configuration id is not valid to update!!"
					}
					)
			final_result = []
			final_result.append(serializer.data)
			return Response({
						"success": True, 
						"message": info_msg,
						"data": final_result,
						})
		except Exception as e:
			print("Analytics action Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})