from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
from rest_framework import serializers
from Configuration.models import PaymentDetails
from ZapioApi.Api.BrandApi.paymentsetting.serializer import PaymentSerializer


class PaymentRetrieve(APIView):
	"""
	Percent Combo retrieval POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for retrieve the payment Configuration.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success"  : True, 
			"message"  : "Percent Combo retrieval api worked well!!",
			"data"     : final_result
		}

	"""
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			record = PaymentDetails.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
					{
						"status": False,
	 					"message": "Payment Configuration data is not valid to update!!"
					})
			else:
				payment_serializer = PaymentSerializer(record, many=True)
				return Response({
						"status": True, 
						"message": "Payment Configuration data updation api worked well!!",
						"data": payment_serializer.data
						})
		except Exception as e:
			print("Payment Configuration retrieval Api Stucked into exception!!")
			print(e)
			return Response({
							"status": False, 
							"message": "Error happened!!", 
							"errors": str(e)})