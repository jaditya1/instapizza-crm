from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
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
from Product.models import Product
from rest_framework.permissions import IsAuthenticated
from UserRole.models import ManagerProfile,UserType
from ZapioApi.api_packages import *
import requests 
from History.models import CouponUsed
from Outlet.models import OutletProfile
from Location.models import *
from zapio.settings import Media_Path
from Customers.models import CustomerProfile
from django.template.loader import render_to_string
from Outlet.models import OutletMilesRules
from frontApi.order.error_radious_check import check_circle

class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = '__all__'

class CouponUsedSerializer(serializers.ModelSerializer):
	class Meta:
		model = CouponUsed
		fields = '__all__' 


def genrate_invoice_number(number):
	length = len(str(number))
	if length < 6:
		aa = 6 - length
		for a in range(aa):
			number = "0" + str(number)
	return str(number)

def order_registration_notification(orderID,oid):
	orderdata = Order.objects.filter(id=orderID).first()
	alldata = {}
	y = orderdata.address
	x = orderdata.customer
	if x != None:
		if 'name' in x:
			alldata['customer'] = x['name']
		else:
			alldata['customer'] = ''

		if 'mobile' in x:
			alldata['mobile'] = x['mobile']
		else:
			alldata['mobile'] = ''

		if 'email' in x:
			alldata['email'] = x['email']
		else:
			alldata['email'] = ''

		if 'address' in x:
			alldata['address'] = x['address']
		else:
			alldata['address'] = ''
	else:
		alldata['customer'] = ''
		alldata['mobile'] = ''
		alldata['email'] = ''
		alldata['address'] = ''
	


	alldata['company'] = orderdata.Company.id
	chkuser = CustomerProfile.objects.filter(Q(mobile=alldata['mobile']),\
						Q(company=alldata['company']))
	if chkuser.count() > 0:
		a = {}
		cadr = chkuser[0].address1
		for k in y:
			alls = {}
			nl = k['locality']
			na = k['address']
			alls['locality'] = nl
			alls['address'] = na
			cadr.append(alls)

		seen = set()
		new_l = []
		for d in cadr:
			t = tuple(d.items())
			if t not in seen:
				seen.add(t)
				new_l.append(d)
		a['address1'] = new_l
		customer_registration_serializer = CustomerSignUpSerializer(chkuser[0],data=a,partial=True)
		if customer_registration_serializer.is_valid():
			customer_data_save = customer_registration_serializer.save()
		else:
			print("aaaaaaa",customer_registration_serializer.errors)


	else:
		cust_data = {}
		cust_data['mobile']	= alldata['mobile']
		cust_data['email']	= alldata['email']
		cust_data['company'] = alldata['company']
		cust_data['address']  = alldata['address']
		cust_data['name']  =	alldata['customer'] 
		cust_data['address1']  = y
		cust_data['pass_pin'] = otp_generator()
		username = str(cust_data['company']) + str(cust_data['mobile'])
		cust_data['username'] = username
		cust_data['active_status'] = 1
		create_user = User.objects.create_user(
			username=username,
			email=cust_data['email'],
			password=cust_data['pass_pin'],
			is_staff=False,
			is_active=True
			)
		if create_user:
			cust_data["auth_user"] = create_user.id
			customer_registration_serializer = CustomerSignUpSerializer(data=cust_data)
			if customer_registration_serializer.is_valid():
				customer_data_save = customer_registration_serializer.save()
			else:
				print("error",customer_registration_serializer.errors)
		else:
			pass

def order_email_notification(orderID,oid,datas):
	url = "https://us-central1-ipos-ivr.cloudfunctions.net/emailNotification/"
	headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
	response= requests.post(url,data=json.dumps(datas),headers=headers)


class OrderProcess(LoggingMixin,APIView):
	"""
	Customer Order POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to save all order related
		data to store it in database for future reference.

		Data Post:  {
			"customer": {
						"name": "umesh",
						"mobile": "8423845784",
						"email" : "umeshsamal3@gmail.com"
						"locality": "adadasd"
						},

			"address1": {
						"city":"Greater Noida",
						"state":"UP",
						"address":"Fusion Homes",
						"pincode":"152365",
						"landmark":"Teen Murti",
						"latitude":28.5995288,
						"longitude":77.44454669999999
						},

			"address_required" : True,

			settlement_details:[
						{"mode":"0","amount":250},
						{"mode":"1","amount":150,"trannsaction_id":"razr_012365478uytre"}
						],

			"order_description": [
									{
							"name": "Margreeta Pizza",
							"id": "12",
							"price": "229",
							"size": "N/A",
							"customization_details": []
						
							},
							{
							"name": "Margreeta Pizza",
							"id": "12",
							"price": "229",
							"size": "N/A",
							"customization_details": []
						
							}
						],
			
			"payment_mode": "1",
			"payment_id" : "Razor1539587456980",
			"Payment_status" : "1",
			"discount_value": 0,
			"total_bill_value": 309,
			"total_items": 2,
			"sub_total": 294,
			"cart_discount": 0,
			"discount_name": "",
			"discount_reason": "",
			"Delivery_Charge": 309,
			"Packing_Charge": 0,
			"Order_Type": "takeaway",
			"Payment_source":"paytm",
			"Order_Source" : "call",
			"delivery_instructions": "asdsadsa",
			"special_instructions": "dasdsadsa",
			"outlet_id" : 3,
			"taxes": 15,
		}

		Response: {

			"success": true,
			"message": "Order Received successfully"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			orderdata = {}
			user = request.user
			shop_check = OutletProfile.objects.filter(id=data['outlet_id'])
			co_id = shop_check[0].Company_id
			err_message = {}
			orderdata['Company'] = co_id
			err_message["Order_Type"] = \
								validation_master_anything(data["Order_Type"],"Order Type",
								alpha_re,3)
			sdetails = data["settlement_details"]
			if len(sdetails) > 0:
				for i in sdetails:
					if 'mode' in i and 'amount' in i:
						pass
					else:
						err_message["payment_detail"] = "Order mode and amount value is not set!!"
						break
					if i['mode'] != 0:
						if 'mode' in i and 'amount' in i and 'transaction_id' in i:
							orderdata['transaction_id'] = i['transaction_id']
						else:
							err_message["payment_detail"] = "Order mode and amount and trannsaction_id value is not set!!"
							break
					else:
						pass
					if i['mode'] == 0:
						orderdata['payment_mode'] = str(0)
					elif i['mode'] == 1:
						orderdata['payment_mode'] = str(1)
					elif i['mode'] == 2:
						orderdata['payment_mode'] = str(2)
					elif i['mode'] == 3:
						orderdata['payment_mode'] = str(3)
					elif i['mode'] == 4:
						orderdata['payment_mode'] = str(4)
					elif i['mode'] == 5:
						orderdata['payment_mode'] = str(5)
					elif i['mode'] == 6:
						orderdata['payment_mode'] = str(6)
					elif i['mode'] == 7:
						orderdata['payment_mode'] = str(7)
					elif i['mode'] == 7:
						orderdata['payment_mode'] = str(8)
					elif i['mode'] == 9:
						orderdata['payment_mode'] = str(9)
					else:
						pass
			else:
				pass

			try:
				data["taxes"] = float(data["taxes"])
			except Exception as e:
				err_message["tax"] = "Tax Price value is not valid!!"

			try:
				data["Delivery_Charge"] = float(data["Delivery_Charge"])
			except Exception as e:
				err_message["Delivery_Charge"] = "Delivery Price value is not valid!!"

			try:
				data["Packing_Charge"] = float(data["Packing_Charge"])
			except Exception as e:
				err_message["Packing_Charge"] = "Packing Price value is not valid!!"

			try:
				data["cart_discount"] = float(data["cart_discount"])
			except Exception as e:
				err_message["cart_discount"] = "Discount value is not valid!!"

			try:
				data["sub_total"] = float(data["sub_total"])
			except Exception as e:
				err_message["sub_total"] = "Sub total value is not valid!!"

			if data["address_required"] == True:
				address = data["address1"]
				if "city" in address:
					err_message["City"] = \
					only_required(address['city'], "City")
				else:
					err_message["City"] = "City is not provided in address!!"

				if "state" in address:
					err_message["state"] = \
						only_required(address['state'], "state")
				else:
					err_message["state"] = "State is not provided in address!!"
				if "latitude" in address:
					err_message["latitude"] = \
						only_required(str(address['latitude']), "latitude")
				else:
					err_message["latitude"] = "Latitude is required in address!!"
				if "longitude" in address:
					err_message["longitude"] = \
					only_required(str(address['longitude']), "longitude")
				else:
					err_message["longitude"] = "Longitude is required in address!!"
				if "address" in address:
					err_message["address"] = \
						only_required(address['address'], "address")
				else:
					err_message["address"] = "Address is not provided!!"
				if 'landmark' in address:
					err_message["landmark"] = \
						only_required(address['landmark'], "landmark")
				else:
					pass
				if "pincode" in address:
					err_message["pincode"] = \
					only_required(address['pincode'], "pincode")
				else:
					err_message["pincode"] = "Pincode is not provided in address!!"
			else:
				pass
			if any(err_message.values())==True:
				return Response({
								"success": False,
								"error" : err_message,
								"message" : "Please correct listed errors!!"
							})

			if data["address_required"] == True and data["Order_Type"] == "Delivery":
				distance_check = {}
				distance_check["shop_id"] = data["outlet_id"]
				distance_check["lat"] = address["latitude"]
				distance_check["long"] = address["longitude"]
				service_check = check_circle(distance_check)
				if service_check == None:
					pass
				else:
					return Response(service_check)
			else:
				pass
			orderdata['order_description'] = data['order_description']
			orderdata['customer'] = data['customer']
			orderdata['order_time'] = datetime.now()
			orderdata['taxes'] = data['taxes']
			orderdata['delivery_instructions'] = data['delivery_instructions']
			orderdata['special_instructions'] = data['special_instructions']
			if len(data['settlement_details']) > 0:
				Order_status_q = OrderStatusType.objects.filter(Order_staus_name__icontains='Settle')
			else:
				Order_status_q = OrderStatusType.objects.filter(Order_staus_name__icontains='Received')
			orderdata['order_status'] = Order_status_q[0].id
			orderdata['sub_total'] = data['sub_total']
			orderdata['discount_value'] = data['cart_discount']
			orderdata['total_bill_value'] = \
			(orderdata['sub_total'] - orderdata['discount_value']) + orderdata['taxes']
			orderdata['outlet'] = str(data['outlet_id'])
			orderdata['settlement_details'] = data['settlement_details']
			orderdata['payment_source'] = data['Payment_source']
			orderdata['order_source'] = data['Order_Source']
			orderdata['packing_charge'] = data['Packing_Charge']
			orderdata['delivery_charge'] = data['Delivery_Charge']
			orderdata['order_type'] = data['Order_Type']
			if "id" in data:
				record = Order.objects.filter(id=str(data['id']))
				if record.count() == 0:
					return Response(
					{
						"success": False,
						"message": "Order data is not valid to update!!"
					}
					)
				else:					
					order_serializer = OrderSerializer(record[0],data=orderdata,partial=True)
					if order_serializer.is_valid():
						order_serializer.save()
						return Response({
									"success":True,
									"message":"Order Updated successfully"
									})
					else:
						return Response({
								"success":False,
								"message":str(usedcoupon_serializer.errors)
								})	

			else:
				company_query = Company.objects.filter(id=co_id)
				last_id_q = Order.objects.filter(Company_id=co_id).last()
				if last_id_q:
					last_id = str(last_id_q.id)
				else:
					last_id = '001'
				city = OutletProfile.objects.filter(id=data['outlet_id'])[0].city_id
				state = CityMaster.objects.filter(id=city)[0].state_id
				sn = StateMaster.objects.filter(id=state)[0].short_name
				out_id = data['outlet_id']
				outlet_wise_order_count = Order.objects.filter(Q(Company_id=orderdata['Company']),Q(outlet_id=data['outlet_id'])).count()
				if outlet_wise_order_count > 0:
					final_outlet_wise_order_count = int(outlet_wise_order_count) + 1
				else:
					final_outlet_wise_order_count = 1
					
				a = genrate_invoice_number(final_outlet_wise_order_count)
				finalorderid = str(sn)+str(out_id)+'-'+str(2021)+str(a)

				orderdata['user']  = \
				ManagerProfile.objects.filter(auth_user_id = user.id)[0].username
				company_name = company_query[0].company_name
				orderdata['order_id'] = company_name+last_id
				orderdata['outlet_order_id'] = finalorderid
				orderdata['order_time'] = datetime.now()
				orderdata['discount_name'] = data['discount_name']
				orderdata['discount_reason'] = data['discount_reason']
				orderdata['address'] = data['address1']
				orderdata["customer"] = data['customer']
				order_serializer = OrderSerializer(data=orderdata)
				if order_serializer.is_valid():
					order_serializer.save()
					orderid = order_serializer.data['id']
					oid = order_serializer.data['order_id']
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
						used_coupon["Company"] = data['company_id']
						used_coupon["created_at"] = datetime.now()
						usedcoupon_serializer = \
						CouponUsedSerializer(data=used_coupon)
						if usedcoupon_serializer.is_valid():
							usedcoupon_serializer.save()
						else:
							print(str(order_serializer.errors))
							return Response({
									"success":False,
									"message":str(usedcoupon_serializer.errors)
									})
					
					order_tracking = \
					OrderTracking.objects.create(order_id=orderid, 
						Order_staus_name_id=orderdata['order_status'], created_at=datetime.now())
					return Response({
									"success":True,
									"message":"Order Received successfully"
									})
				else:
					return Response({"success":False,
									"message":str(order_serializer.errors)})
		except Exception as e:
			return Response({
							"success"	: 	False,
							"message"	:	"Order place api stucked into exception!!",
							"error" 	:	str(e) 
							})
