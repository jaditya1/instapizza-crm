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
from ZapioApi.Api.BrandApi.analyticsSetting.serializer import AnalyticsSerializer
from django.db.models import Q
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

class AnalyticsEdit(APIView):

	"""
	Analytics Configuration Edit POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to edit the Analytics Configuration details.

		Data Post: {
		    "u_id"                    : "#fasdfasdagfdgercrfgrbrtrbtfvefvvfebfebeffd600",
    		"analytics_snippets"                   : "<html>assssaa</html>",
  			"id"                          : "1"
		}

		Response: {

			"success"  : True, 
			"message"  : "Analytics edit api worked well!!",
			"data"     : final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			auth_id = request.user.id
			Company_id = get_user(auth_id)
			err_message = {}
			err_message["u_id"] =  only_required(data["u_id"],"User Id")
			err_message["analytics_snippets"] =  \
			only_required(data["analytics_snippets"],"Analytics Snippet")
			err_message["id"] = validation_master_anything(str(data["id"]),
								"Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = AnalyticsSetting.objects.filter(Q(id=data['id']),Q(company=Company_id))
			if record.count() == 0:
				return Response(
					{
						"status": False,
	 					"message": "Analytics Configuration data is not valid to update!!"
					})
			else:
				data["updated_at"] = datetime.now()
				serializer = \
					AnalyticsSerializer(record[0],data=data,partial=True)
				if serializer.is_valid():
					data_info = serializer.save()
					return Response({
						"status": True, 
						"message": "Google Analytics Configuration is updated successfully!!",
						"data": serializer.data
						})
				else:
					print("something went wrong!!")
					return Response({
						"status": False, 
						"message": str(serializer.errors),
						})
		except Exception as e:
			print("Google Analytics Configuration retrieval Api Stucked into exception!!")
			print(e)
			return Response({
							"status": False, 
							"message": "Error happened!!", 
							"errors": str(e)})