from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from _thread import start_new_thread
from datetime import datetime
from django.db.models import Q
from Orders.models import Order, OrderStatusType, OrderTracking
import json
from Brands.models import Company
from discount.models import Coupon
from History.models import CouponUsed
from frontApi.serializer.customer_serializers import CustomerSignUpSerializer
from rest_framework_tracking.mixins import LoggingMixin

#Serializer for api
from rest_framework import serializers
import math
from .send_mail import *
from Product.models import Product
# from frontApi.order.Validation.order_error_check import *
from Location.models import *
from frontApi.order.error_radious_check import check_circle

def genrate_invoice_number(number):
	length = len(str(number))
	if length < 6:
		aa = 6 - length
		for a in range(aa):
			number = "0" + str(number)
	return str(number)



class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = '__all__'

class CouponUsedSerializer(serializers.ModelSerializer):
	class Meta:
		model = CouponUsed
		fields = '__all__' 




class OrderData(LoggingMixin,APIView):
	"""
	Customer Order POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to save all order related
		data to store it in database for future reference.

		Data Post:  {
			"customer"				: 		{
												"name"		: 	"umesh",
												"mobile"	: 	"8423845784",
												"email" 	: 	"umeshsamal3@gmail.com"
												"locality"	: 	"adadasd"
											},

			"address"				:		{
												"city"		:	"Greater Noida",
												"state"		:	"UP",
												"address"	:	"Fusion Homes",
												"pincode"	:	"152365",
												"landmark"	:	"Teen Murti",
												"latitude"	:	28.5995288,
												"longitude"	:	77.44454669999999
											},

			"order_description"		: 		[		
											{
					   							"id"		:	379,
					   							"name"		:	"Juicy Juicy Chicken",
					   							"size"		:	"N/A",
					   							"price"		:	175,
					   							"add_ons"	:	[
					      											{
					         										"price":10,
					         										"addon_id":950,
					         										"addon_name":"BBQ Sauce"
					      											},
					      											{
					         										"price":10,
					         										"addon_id":952,
					         										"addon_name":"Peri Peri Sauce"
					      											},
					      											{
					         										"price":10,
					         										"addon_id":954,
					         										"addon_name":"Mint Mayo Sauce"
					      											}
					   											],
					   							"quantity"	:	1
											},
											{
					   							"id"		:	563,
					   							"name"		:	"Peri Peri Onion",
					   							"size"		:	"N/A",
					   							"price"		:	145,
					   							"add_ons"	:	[
					      											{
					         										"price":10,
					         										"addon_id":950,
					         										"addon_name":"BBQ Sauce"
					      											},
					      											{
					         										"price":10,
					         										"addon_id":952,
					         										"addon_name":"Peri Peri Sauce"
					      											},
					      											{
					         										"price":10,
					         										"addon_id":954,
					         										"addon_name":"Mint Mayo Sauce"
					      											}
					   											],
					   							"quantity"	:	1
											}
											]
			
			"payment_mode"			: 		"1",
			"payment_id" 			: 		"Razor1539587456980",
			"Payment_status" 		: 		"1",
			"discount_value"		: 		0,
			"total_bill_value"		: 		309,
			"total_items"			: 		2,
			"sub_total"				: 		294,
			"cart_discount"			: 		0,
			"discount_name"			: 		"",
			"Delivery_Charge"		: 		309,
			"Packing_Charge"		: 		0,
			"Order_Type"			: 		"Delivery",
			"Payment_source"		:		"paytm",
			"Order_Source" 			: 		"Website",
			"delivery_instructions"	: 		"asdsadsa",
			"special_instructions"	: 		"dasdsadsa",
			"shop_id" 				: 		3,
			"taxes"					: 		15,
		}



		Response: {

			"success": true,
			"message": "Order Received successfully"
		}

	"""
	def post(self, request, format=None):
		try:
			post_data = request.data
			if int(post_data["payment_mode"]) == 0:
				return Response({
					"success"	:	False,
					"message"	:	"Sorry....we are not accepting COD orders now!!"
					})
			else:
				pass

			address = post_data["address"]
			# if "latitude" in address and "longitude" in address and "pincode" in address:
			# 	pass
			# else:
			# 	 return Response({
			# 		"success"	:	False,
			# 		"message"	:	"Please provide proper customer address!!"
			# 		})
			distance_check = {}
			distance_check["shop_id"] = post_data["shop_id"]
			distance_check["lat"] = address["latitude"]
			distance_check["long"] = address["longitude"]
			# service_check = check_circle(distance_check)
			# if service_check == None:
			# 	pass
			# else:
			# 	return Response(service_check)
			orderdata = {}
			orderdata['order_description'] = post_data['order_description']
			pdata = orderdata['order_description']
			dataorder = len(pdata)
			pro_id = pdata[0]['id'] 
			cid = Product.objects.filter(id=pro_id).first().Company_id
			orderdata['Company_outlet_details'] = post_data['Company_outlet_details']
			orderdata['address'] =  post_data['address']
			orderdata['customer'] = post_data['customer']
			company_query = Company.objects.filter(id=cid)
			post_data["company_name"] = company_query[0].company_name
			last_id_q = Order.objects.filter(Company_id=cid).last()
			if last_id_q:
				last_id = str(last_id_q.id)
			else:
				last_id = '001'
			
			last_oid_q = Order.objects.filter(outlet_id=post_data['shop_id']).last()
			city = OutletProfile.objects.filter(id=post_data['shop_id'])[0].city_id
			state = CityMaster.objects.filter(id=city)[0].state_id
			sn = StateMaster.objects.filter(id=state)[0].short_name
			out_id = post_data['shop_id']
			outlet_wise_order_count = Order.objects.filter(Q(Company_id=cid),Q(outlet_id=post_data['shop_id'])).count()
			if outlet_wise_order_count > 0:
				final_outlet_wise_order_count = int(outlet_wise_order_count) + 1
			else:
				final_outlet_wise_order_count = 1
			# finalorderid = str(sn)+'-'+str(out_id)+'-'+str(2021)+'-'+str(final_outlet_wise_order_count)
			a = genrate_invoice_number(final_outlet_wise_order_count)
			finalorderid = str(sn)+str(out_id)+'-'+str(2021)+str(a)
			company_name = company_query[0].company_name
			orderdata['order_id'] = company_name+last_id
			orderdata['outlet_order_id'] = finalorderid
			orderdata['order_description'] = post_data['order_description']
			orderdata['order_time'] = post_data['order_time']
			orderdata['taxes'] = post_data['taxes']
			orderdata['delivery_instructions'] = post_data['delivery_instructions']
			orderdata['special_instructions'] = post_data['special_instructions']
			orderdata['payment_mode'] = post_data['payment_mode']
			Order_status_q = OrderStatusType.objects.filter(Order_staus_name__icontains='Received')
			orderdata['order_status'] = Order_status_q[0].id
			orderdata['sub_total'] = post_data['sub_total']
			orderdata['discount_value'] = post_data['discount_value']
			orderdata['transaction_id'] = post_data['payment_id']
			orderdata['coupon_code'] = post_data['coupon_code']
			orderdata['is_paid'] = post_data['Payment_status']
			orderdata['total_bill_value'] = post_data['total_bill_value']
			orderdata['total_items']  = post_data['total_items']
			if post_data['total_items'] != "" and post_data['total_items'] != None:
				pass
			else:
				orderdata['total_items'] = len(post_data['order_description']) 
			orderdata['outlet'] = post_data['shop_id']
			orderdata['order_source'] = post_data['order_source']
			orderdata['Company'] = cid
			orderdata['user'] = Company.objects.filter(id=cid)[0].username
			order_record = Order.objects.filter(Company=orderdata['Company'])
			if order_record.count() != 0:
				is_visited = order_record.\
				filter(customer__mobile_number=post_data['customer']['mobile_number'])
				if is_visited.count() == 0:
					pass
				else:
					orderdata['has_been_here'] = 1
					is_visited.update(has_been_here=1)
			else:
				pass
			order_serializer = OrderSerializer(data=orderdata)
			if order_serializer.is_valid():
				order_serializer.save()
				orderid = order_serializer.data['id']
				oid = order_serializer.data['outlet_order_id']
				start_new_thread(order_email_notification, (orderid,oid,post_data))
				start_new_thread(order_registration_notification, (orderid,oid))
				ccode = Order.objects.filter(id=orderid).first().coupon_code
				if ccode == "" or ccode==None:
					pass
				else:
					code_check = Coupon.objects.\
					filter(coupon_code__exact=ccode,active_status=1)
					if code_check.count() != 0:
						frequency = code_check[0].frequency
						updated_freq = frequency - 1
						code_update_q = code_check.update(frequency=updated_freq)
					else:
						pass
					used_coupon = {}
					used_coupon["Coupon"] = code_check[0].id
					used_coupon["customer"] = orderdata['customer']
					used_coupon["order_id"] = orderid
					used_coupon["Company"] = orderdata['Company']
					used_coupon["outlet"] = orderdata['outlet']
					used_coupon["created_at"] = datetime.now()
					usedcoupon_serializer = \
					CouponUsedSerializer(data=used_coupon)
					if usedcoupon_serializer.is_valid():
						usedcoupon_serializer.save()
					else:
						return Response({
								"success":False,
								"message":str(usedcoupon_serializer.errors)
								})
				order_tracking = \
				OrderTracking.objects.create(order_id=orderid, 
					Order_staus_name_id=orderdata['order_status'], created_at=datetime.now())
				# start_new_thread(order_confirmation, (orderid,cid))
				return Response({
								"success":True,
								"message":"Order Received successfully"
								})
			else:
				return Response({"success":False,
								"message":str(order_serializer.errors)})
		except Exception as e:
			return Response({"success": False,
							"message":"Order place api stucked into exception!!"})