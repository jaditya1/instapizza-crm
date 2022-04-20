from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
from rest_framework import serializers
from pos.models import POSOrder
from datetime import datetime, timedelta


class PosRetrieve(APIView):
	"""
	Pos retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of pos data..

		Data Post: {
			"id"                   : "3"
		}

		Response: {

			"success": True, 
			"message": "POS retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			data["id"] = str(data["id"])
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"POS Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})

			pos_record = POSOrder.objects.filter(id=data['id'])
			if pos_record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Required Pos data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				alld = {}
				alld['created_on'] = pos_record[0].created_on.strftime("%d %b %Y")
				alld['customer_name'] = pos_record[0].customer_name
				alld['customer_number'] = pos_record[0].customer_number
				alld['date'] = pos_record[0].date.strftime("%d %b %Y")
				alld['discount_value'] = pos_record[0].discount_value
				alld['external_id'] = pos_record[0].external_id
				alld['ids'] = pos_record[0].ids
				alld['invoice_number'] = pos_record[0].invoice_number
				alld['order_type'] = pos_record[0].order_type
				alld['outlet'] = pos_record[0].outlet
				alld['payment_mode'] = pos_record[0].payment_mode
				alld['rider_name'] = pos_record[0].rider_name
				alld['rider_number'] = pos_record[0].rider_number
				alld['source'] = pos_record[0].source
				alld['status_name'] = pos_record[0].status_name
				alld['sub_total'] = pos_record[0].sub_total
				alld['time'] = pos_record[0].time
				alld['total'] = pos_record[0].total
				alld['total_tax'] = pos_record[0].total_tax
				alld['user_name'] = pos_record[0].user_name
			return Response({
						"success": True, 
						"message": "POS retrieval api worked well!!",
						"data": alld,
						})
		except Exception as e:
			print("POS retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
