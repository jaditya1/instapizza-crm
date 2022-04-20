from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, \
	HTTP_406_NOT_ACCEPTABLE, HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import re
from ZapioApi.api_packages import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from _thread import start_new_thread
from datetime import datetime
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from Orders.models import Order, OrderStatusType, OrderTracking
import json
from Outlet.models import OutletProfile,DeliveryBoy
from Brands.models import Company
from rest_framework import serializers
from OutletApi.Api.serializers.order_serializers import BoySerializer,OrderTrackSerializer, OrderSerializer
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import ChangestatusData


class ChangeStatusData(APIView):
	"""
	Order Change status POST API
		Authentication Required		: No
		Service Usage & Description	: This Api is used to save all order status change API.
		Data Post: {
				"order_id" 		   : "1"
		}
		Response: {
			"success": True, 
			"message" : "Order Status changed successfully!!",
		}

	"""
	def post(self, request, format=None):
		try:
			data = request.data
			ret_check = ChangestatusData(data)
			if ret_check !=None:
				return Response(ret_check) 
			else:
				pass

			
		except Exception as e:
			print(e)
			return Response({
						"success": False,
						"error" : str(e),
						"message" : "Please correct listed errors!!"
						})