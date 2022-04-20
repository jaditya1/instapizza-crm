from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime, timedelta
from django.db.models import Q
import os
from django.db.models import Max
import dateutil.parser

from rest_framework import serializers
from pos.models import POSOrder


# class CouponSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = Coupon
# 		fields = '__all__'


class PosListData(APIView):
	"""
	POS Order list data POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to list of POS order data within brand.

		Data Post: {
			"start_date"            : "2019-07-24 00:00:00:00",
			"end_date"              : "2019-07-29 00:00:00:00"
		}

		Response: {

			"success": True, 
			"message": "List Of POS Order data api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			mutable = request.POST._mutable
			request.POST._mutable = True
			err_message = {}
			start_date = data['start_date']
			end_date = data['end_date']
			if data["start_date"] != '' and data["end_date"] != '':
				start_date = dateutil.parser.parse(data["start_date"])
				end_date = dateutil.parser.parse(data["end_date"])
				if start_date > end_date:
					err_message["from_till"] = "Validity dates are not valid!!"
			else:
				pass
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			if data["start_date"] != '' and data["end_date"] != '':
				alldata = POSOrder.objects.filter(Q(date__lte=end_date),Q(date__gte=start_date))
			else:
				alldata = POSOrder.objects.filter()
			final_result = []
			if alldata.count() > 0:
				for i in alldata:
					alld = {}
					alld['id'] = i.id
					alld['created_on'] = i.created_on.strftime("%d %b %Y")
					alld['customer_name'] = i.customer_name
					alld['customer_number'] = i.customer_number
					alld['date'] = i.date.strftime("%d %b %Y")
					alld['discount_value'] = i.discount_value
					alld['external_id'] = i.external_id
					alld['ids'] = i.ids
					alld['invoice_number'] = i.invoice_number
					alld['order_type'] = i.order_type
					alld['outlet'] = i.outlet
					alld['payment_mode'] = i.payment_mode
					alld['rider_name'] = i.rider_name
					alld['rider_number'] = i.rider_number
					alld['source'] = i.source
					alld['status_name'] = i.status_name
					alld['sub_total'] = i.sub_total
					alld['time'] = i.time
					alld['total'] = i.total
					alld['total_tax'] = i.total_tax
					alld['user_name'] = i.user_name
					final_result.append(alld)
			return Response({
						"success": True, 
						"data": final_result,
						})
		except Exception as e:
			print("POS data Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


