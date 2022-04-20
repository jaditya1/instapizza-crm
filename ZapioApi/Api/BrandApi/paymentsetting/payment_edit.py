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

class PaymentEdit(APIView):
	"""
	Percent Combo retrieval POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for edit the payment Configuration.

		Data Post: {
		    "keyid"                : "rzp_live_xcgVtA1lIkJ",
    		"keySecret"            : "dgwbqAGqDcFXNRBYkXaP",
    		"symbol"			   : "INR"
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
				data["updated_at"] = datetime.now()
				payment_serializer = \
					PaymentSerializer(record[0],data=data,partial=True)
				if payment_serializer.is_valid():
					data_info = payment_serializer.save()
					return Response({
						"status": True, 
						"message": "Payment credentials are updated successfully!!",
						"data": payment_serializer.data
						})
				else:
					print("something went wrong!!")
					return Response({
						"status": False, 
						"message": str(payment_serializer.errors),
						})
		except Exception as e:
			print("Payment Configuration retrieval Api Stucked into exception!!")
			print(e)
			return Response({
							"status": False, 
							"message": "Error happened!!", 
							"errors": str(e)})