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
from Product.models import Product, AddonDetails, Tag,Variant
from django.db.models import Q
from Configuration.models import TaxSetting
from Orders.models import Order

class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = '__all__'


class OrderRetrieve(APIView):
	"""
	Order retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Order data.

		Data Post: {
			"id"                   : "60"
		}

		Response: {

			"success": True, 
			"message": "Order retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			data['id'] = str(data['id'])
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Order Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = Order.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided Order data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["invoice_id"] = record[0].outlet_order_id
				q_dict["total_bill_value"] = record[0].total_bill_value
				q_dict["transaction_id"] = record[0].transaction_id
				q_dict["order_source"] = []
				od_dict = {}
				od_dict["value"]  =   record[0].order_source
				od_dict["key"]    =    record[0].order_source
				od_dict["label"]  =    record[0].order_source
				q_dict["order_source"].append(od_dict)
				q_dict["order_status"] = []
				ost = {}
				ost["value"]  =   record[0].order_status_id
				ost["key"]    =    record[0].order_status_id
				ost["label"]  =    record[0].order_status.Order_staus_name
				q_dict["order_status"].append(ost)
				mode_detail = record[0].settlement_details
				q_dict["payment_mode_details"] = []
				if mode_detail != None:
					for q in mode_detail:
						mode_dict = {}
						mode = int(q['mode'])
						amount = float(q['amount'])
						if mode == 0:
							md = 'Cash on Delivery'
						elif mode == 1:
							md = 'Dineout'
						elif mode == 2:
							md = 'Paytm'
						elif mode == 3:
							md = 'Razorpay'
						elif mode == 4:
							md = 'PayU'
						elif mode == 5:
							md = 'EDC'
						elif mode == 6:
							md = 'Mobiquik'
						elif mode == 7:
							md = 'Mix'
						elif mode == 8:
							md = 'EDC Amex'
						elif mode == 9:
							md = 'EDC Yes Bank'
						elif mode == 10:
							md = 'swiggy'
						elif mode == 11:
							md = 'Z Prepaid'
						elif mode == 12:
							md = 'S Prepaid'
						elif mode == 13:
							md = 'Dunzo'
						elif mode == 14:
							md = 'Zomato Cash'
						elif mode == 15:
							md = 'Zomato'
						elif mode == 16:
							md = 'Magic Pin'
						elif mode == 17:
							md = 'Easy Dinner'
						if 'transaction_id' in q:
							trans_id = q['transaction_id']
						else:
							trans_id = None
						if mode == 0:
							trans_required = False
						elif mode == 14:
							trans_required = False
						elif mode == 10:
							trans_required = False
						elif mode == 15:
							trans_required = False
						else:
							trans_required = True
						mode_dict["value"] 	=   q['mode']
						mode_dict["key"]    =   q['mode']
						mode_dict["label"]  =   md
						mode_dict["transaction_id"] = trans_id 
						mode_dict["amount"] = amount
						mode_dict["trans_required"] = trans_required
						q_dict["payment_mode_details"].append(mode_dict)
				else:
					pass
				final_result.append(q_dict)
				return Response({
							"success"	: 	True, 
							"message"	: 	"Order retrieval api worked well!!",
							"data"		: 	final_result,
							})
		except Exception as e:
			return Response({
				"success"	: 	False, 
				"message"	: 	"Error happened!!", 
				"errors"	: 	str(e)
				})



