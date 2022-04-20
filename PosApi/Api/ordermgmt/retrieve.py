from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime, timedelta
from Orders.models import Order,OrderStatusType
from Product.models import Product
#Serializer for api
from rest_framework import serializers
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import RetrievalData


def custom_decorator(function):
	def inner(func,func1):
		if "id" in func1.data:
			return function(func,func1)
		else:
			return Response({
				"success": False
				})
	return inner
	

class BrandOrderRetrieval(APIView):
	"""
	Order retrieval at POS Level POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of order data within outlet.

		Data Post: {
			"id"                   : "3"
		}

		Response: {

			"success": True, 
			"message": "Order data retrieval api worked well!!",
			"data": final_result
		}

	"""


	permission_classes = (IsAuthenticated,)
	# @custom_decorator
	def post(self, request, format=None):
		try:
			data = request.data
			ret_check = RetrievalData(data)
			if ret_check !=None:
				return Response(ret_check) 
			else:
				return Response({
					"success"	:	False
					})
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})

