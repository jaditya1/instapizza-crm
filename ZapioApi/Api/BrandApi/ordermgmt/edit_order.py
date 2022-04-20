from rest_framework.views import APIView
from rest_framework.response import Response
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime
from Orders.models import Order,OrderTracking
from rest_framework_tracking.mixins import LoggingMixin


valid_modes = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]

class EditOrder(LoggingMixin,APIView):

	"""
	Edit Order POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to edit order post api.

		Data Post: {
			"order_status" 			: 		"",
			"settlement_details"	:			[
										{"mode":"0","amount":250},
										{"mode":"1","amount":150,"transaction_id":"razr_012365478uytre"}
										]
			"order_source" 			: 		"",
			"order_id"     			: 		"947"
			"transaction"   		: 		"4243243243223"
		}

		Response: {

			"success"	: 		True, 
			"message"	: 		"Order Updated Successfully!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			err_message = {}
			sdetails = data["settlement_details"]
			total_amount = 0
			unique_mode_list = []
			if len(sdetails) > 0:
				for i in sdetails:
					if 'mode' in i and 'amount' in i:
						i["mode"] = str(i["mode"])
					else:
						err_message["payment_detail"] = "Order mode and amount value is not set!!"
						break
					if i['mode'] != 0:
						if 'mode' in i and 'amount' in i and 'transaction_id' in i:
							pass
						else:
							err_message["payment_detail"] = "Order mode and amount and transaction_id value is not set!!"
							break
					else:
						pass
					if i["mode"] in unique_mode_list:
						err_message["mode"] = "Payment mode is duplicate!!"
						break
					else:
						unique_mode_list.append(i["mode"])
					if i["mode"] == "0":
						err_message["mode"] = None
					else:
						err_message["mode"] = validation_master_anything(i["mode"],
											"Mode Id",contact_re, 1)
					if err_message["mode"] == None:
						pass
					else:
						break
					try:
						total_amount = total_amount+float(i["amount"])
					except Exception as e:
						err_message["amount"] = "Settlement amount is not valid!!"
						break
					if int(i["mode"]) in valid_modes:
						pass
					else:
						err_message["mode"] = "Payment Mode is not valid!!"
						break

			else:
				err_message["settlement_details"] = "Settlement details are not provided!!"
			err_message["order_status"] = validation_master_anything(str(data["order_status"]),
											"Order Status",contact_re, 1)
			err_message["order_id"] = validation_master_anything(str(data["order_id"]),
											"Order Id",contact_re, 1)
			if err_message["order_status"] == None:
				if int(data["order_status"]) != 6 and int(data["order_status"]) != 7:
					err_message["order_status"] = "Order status can'nt be changed other than 'settled' or 'cancelled'!!"
				else:
					pass
			else:
				pass
			err_message["order_source"] = only_required(data["order_source"], \
															"Order Source")
			if any(err_message.values())==True:
				return Response({
					"success"	: 	False,
					"error" 	:	err_message,
					"message" 	: 	"Please correct listed errors!!"
					})
			record = Order.objects.filter(id=data['order_id'])
			if record.count() == 0:
				return Response({
					"success": False,
 					"message": "Provided Order data is not valid to retrieve!!"
				})
			else:
				pass
			q = record[0]
			# if q.order_status_id != 6 and q.order_status_id != 7:
			# 	err_message["order_status"] = "This order can'nt be edited right now!!"
			# 	return Response({
			# 		"success"	: 	False,
			# 		"error" 	:	err_message,
			# 		"message" 	: 	"Please correct listed errors!!"
			# 		})
			# else:
			# 	pass
			if total_amount == q.total_bill_value:
				pass
			else:
				err_message["order_status"] = "Settlement value is not matching!!"
				return Response({
					"success"	: 	False,
					"error" 	:	err_message,
					"message" 	: 	"Please correct listed errors!!"
					})
			if len(sdetails) > 1:
				payment_mode = str(7)
			else:
				payment_mode = str(sdetails[0]['mode'])
				trans_id = str(sdetails[0]["transaction_id"])
			if payment_mode == "14":
				trans_id = "COD"
			elif payment_mode == "0":
				trans_id = "COD"
			else:
				if len(sdetails) == 1:
					pass
				else:
					trans_id = data["transaction"]
			if q.discount_name == "Complimentary":
				trans_id = "Complimentary"
			else:
				pass
			if data['transaction'] != None and trans_id != "Complimentary" and trans_id != "COD":
				trans_id = data["transaction"]
			else:
				pass
			update_data = \
				record.update(settlement_details=sdetails,transaction_id=trans_id,\
				order_status=data['order_status'],order_source=data["order_source"],\
				payment_mode=payment_mode)
			if update_data:
				chk_type = \
				OrderTracking.objects.filter(Order_staus_name_id = data['order_status'],\
														order_id=data['order_id'])
				if chk_type.count() > 0:
					pass
				else:
					order_tracking = OrderTracking.objects.create(order_id=data['order_id'], 
					Order_staus_name_id=data['order_status'], created_at=datetime.now())
				if q.order_status_id == 7:
					chk_type = \
					OrderTracking.objects.filter(Order_staus_name = 6,\
												order_id=data['order_id'])
					if chk_type.count() > 0:
						chk_type.delete()
					else:
						pass
				else:
					pass
				if q.order_status_id == 6:
					chk_type = OrderTracking.objects.filter(Order_staus_name = 7,\
														order_id=data['order_id'])
					if chk_type.count() > 0:
						chk_type.delete()
					else:
						pass
				else:
					pass
				return Response({
					"success"	: 	True, 
					"message"	: 	"Order Updated Successfully!!"
					})
			else:
				return Response({
					"success"	: 	False, 
					"message"	: 	"Order updation was unsuccessful!!"
					})
		except Exception as e:
			return Response({
				"success"	: 	False, 
				"message"	: 	"Error happened!!", 
				"errors"	: 	str(e)
				})
