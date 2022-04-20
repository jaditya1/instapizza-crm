from django.utils.html import strip_tags
from zapio.settings import Media_Path
from Outlet.models import OutletProfile
from Brands.models import Company
from Orders.models import Order, OrderStatusType, OrderTracking
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from _thread import start_new_thread
from Customers.models import CustomerProfile
from django.db.models import Q
from frontApi.serializer.customer_serializers import CustomerSignUpSerializer
from Configuration.models import ColorSetting,EmailSetting
from datetime import datetime
import requests 
import json


secret_token = "83c1e2c6ab0cb1fded654cbb1662b350b4a058b11d38576c125925a1f0d00a1e"

def email_send_module(toe,send_data,company_id):
	order_mail = Company.objects.filter(id=company_id)[0].support_person_email_id
	url = "https://jaditya.pythonanywhere.com/api/mailservice/insta/"
	data = {}
	data["mail_content"] = send_data
	data["primary_mail"] = toe
	data["secondary_mail"] = order_mail
	data["subject"] = "Order Summary"
	data["type"] = "order"
	headers = {}
	headers["token"] = secret_token
	headers["Content-Type"] = "application/json"
	response = requests.request("POST", url, data=json.dumps(data), headers=headers)
	response_data = response.json()
	if response_data["success"] == True:
		is_delivered = True
	else:
		is_delivered = False
	return "mail_sent"


def email_user_send_module(toe,send_data):
	try:
		url = "https://jaditya.pythonanywhere.com/api/mailservice/insta/"
		# url = "http://192.168.0.6:8080/api/mailservice/insta/"
		data = {}
		data["mail_content"] = send_data
		data["primary_mail"] = toe
		data["secondary_mail"] = ""
		data["subject"] = "Registration Detail"
		data["type"] = "registration"
		subject = "Registration Detail"
		headers = {}
		headers["token"] = secret_token
		headers["Content-Type"] = "application/json"
		response = requests.request("POST", url, data=json.dumps(data), headers=headers)
		response_data = response.json()
		if response_data["success"] == True:
			is_delivered = True
		else:
			is_delivered = False
		return "mail_sent"
	except Exception as e:
		print(e)




def order_email_notification(orderID,oid,datas):
	import datetime
	from discount.models import PercentOffers
	orderdata = Order.objects.filter(id=orderID).first()
	company_id = orderdata.Company_id
	today = datetime.datetime.now()
	cname = Company.objects.filter(id=company_id)[0]
	themedata = ColorSetting.objects.filter(company_id=company_id)
	alldata = {}
	alldata['order_time'] = orderdata.order_time
	alldata['taxes'] = str(orderdata.taxes)[:4]
	alldata['payment_mode'] = orderdata.payment_mode
	if alldata['payment_mode'] == "0":
		alldata["trans_id"] = "N/A"
	else:
		alldata["trans_id"] = orderdata.payment_id
	alldata['payment_id'] = orderdata.transaction_id
	alldata['sub_total'] = orderdata.sub_total
	alldata['discount_value'] = orderdata.discount_value
	alldata['total_bill_value'] = orderdata.total_bill_value
	alldata['total_items'] = orderdata.total_items
	alldata['company'] = orderdata.Company.company_logo
	alldata['website'] = orderdata.Company.website
	alldata['shop_id'] = orderdata.outlet_id
	alldata['final'] = Media_Path + str(alldata['company'])
	outletdetails = OutletProfile.objects.filter(id=int(alldata['shop_id'])).first()
	y = orderdata.address
	if 'city' in y.keys():
		alldata['caddress'] = y['address']
	else:
		pass
	if 'locality' in y.keys():
		alldata['locality'] = y['locality']
	else:
		pass
	if 'city' in y.keys():
		alldata['city'] 	= y['city']
	else:
		pass
	if 'longitude' in y.keys():
		alldata['longitude']   = y['longitude']
	else:
		pass
	if 'latitude' in y.keys():
		alldata['latitude'] 	= y['latitude']
	else:
		pass
	x = orderdata.customer
	alldata['customer']       	 = x['name']
	alldata['mobile_number'] 	 = x['mobile_number']
	alldata['email'] 	         = x['email']
	alldata['brand_id']           = x['brand_id']
	alldata['total_orders'] 	  = x['total_orders']
	alldata['first_visit']        = x['first_visit']
	alldata['last_order'] 	      = x['last_order']
	cd = orderdata.order_description

	c = []
	for i in range(len(cd)):
		orderdes={}
		orderdes['name']                  = cd[i]['name']
		orderdes['price'] 				  = cd[i]['price']
		c.append(orderdes)
		cud = cd[i]['add_ons']
		lec = len(cd[i]['add_ons'])
		if lec > 0:
			d = []
			for j in range(lec):
				custodata ={}
				custodata['cname']  = cud[j]['addon_name']
				custodata['cprice'] = cud[j]['price']
				d.append(custodata)
		else:
			pass

	send_data={
				"tax" : alldata['taxes'],
				"patmentmode" : alldata['payment_mode'],
				"payment_id" : alldata['payment_id'],
				"sub_total" : 	alldata['sub_total'],
				"discount_value" : alldata['discount_value'],
				"total_bill_value" : alldata['total_bill_value'],
				"total_items" : alldata['total_items'],
				"logo" : alldata['final'],
				"address1" : alldata['caddress'],
				"locality" : alldata['locality'],
				"city" : alldata['city'] ,
				"customer" : alldata['customer']  ,
				"mobile_number"	 : 	alldata['mobile_number'],
				"emails" 	     : alldata['email'],
				"brand_id"       : alldata['brand_id'],
				"total_orders" 	 : alldata['total_orders'],
				"first_visit"    : alldata['first_visit'],
				"last_order" 	 : 	alldata['last_order'],
				"orderid"        : oid,
				"outletname"     :outletdetails.Outletname,
				"username"		 :outletdetails.username,
				"address":outletdetails.address,
				"city" : outletdetails.city.city,
				"area" : outletdetails.area.area,
				"mobile" : outletdetails.mobile_with_isd,
				"email" : outletdetails.email,
				"order_cart_list":cd,
				"trans_id" : alldata["trans_id"],
				"accent_color" :  themedata[0].accent_color,
				"textColor" :  themedata[0].textColor,
				"secondaryColor" :  themedata[0].secondaryColor,
				"company_name"   : cname.company_name,
				"address"   : cname.address,
				# "content" :  emaildata[0].content,
			}

	datas['company_name'] = cname.company_name
	datas['product_desc'] = cd
	datas['logo'] = alldata['final']
	datas['outlet_name'] = outletdetails.Outletname
	datas['order_id'] = oid
	# url = "https://us-central1-ipos-ivr.cloudfunctions.net/emailNotification/"
	# headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
	# response= requests.post(url,data=json.dumps(datas),headers=headers)
	to_emailID_list = alldata['email'] 
	email_send_status = email_send_module(to_emailID_list,send_data,company_id)



def order_registration_notification(orderID,oid):
	orderdata = Order.objects.filter(id=orderID).first()
	alldata = {}
	alldata['company'] = orderdata.Company.company_logo
	alldata['final'] = Media_Path +"/media/"+ str(alldata['company'])
	alldata['shop_id'] = orderdata.outlet_id
	alldata['final'] = Media_Path + str(alldata['company'])
	outletdetails = OutletProfile.objects.filter(id=int(alldata['shop_id'])).first()
	y = orderdata.address
	alldata['caddress'] = y['address']
	alldata['locality'] = y['locality']
	alldata['city'] 	= y['city']
	alldata['longitude']   = y['longitude']
	alldata['latitude'] 	= y['latitude']
	x = orderdata.customer
	alldata['customer']       	 = x['name']
	alldata['mobile_number'] 	 = x['mobile_number']
	alldata['email'] 	         = x['email']
	alldata['brand_id']           = x['brand_id']
	alldata['total_orders'] 	  = x['total_orders']
	alldata['first_visit']        = x['first_visit']
	alldata['last_order'] 	      = x['last_order']
	alldata['company'] = orderdata.Company.id
	chkuser = CustomerProfile.objects.filter(Q(mobile=alldata['mobile_number']),\
						Q(company=alldata['company']))
	if chkuser.count() > 0:
		pass
	else:
		cust_data = {}
		cust_data['mobile']	= alldata['mobile_number']
		cust_data['email']	= alldata['email']
		cust_data['company'] = alldata['company']
		cust_data['address']  = alldata['caddress']
		cust_data['latitude'] =alldata['latitude']
		cust_data['longitude']  = alldata['longitude']
		cust_data['name']  =	alldata['customer'] 
		cust_data['pass_pin'] = otp_generator()
		username = str(cust_data['company']) + str(cust_data['mobile'])
		cust_data['username'] = username
		cust_data['active_status'] = 1
		create_user = User.objects.create_user(
			username=username,
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
				print(customer_registration_serializer.errors)
			send_data={
						"logo"     : alldata['final'],
						"address1" : alldata['caddress'],
						"locality" : alldata['locality'],
						"customer" : alldata['customer']  ,
						"mobile_number"	 : 	alldata['mobile_number'],
						"emails" 	     : alldata['email'],
						"outletname" :outletdetails.Outletname,
						"username":cust_data['mobile'],
						"address":outletdetails.address,
						"city" : outletdetails.city.city,
						"area" : outletdetails.area.area,
						"mobile" : cust_data['mobile'],
						"email" : cust_data['email'],
						"password" : cust_data['pass_pin'],
						"name" : cust_data['name']  
					}
			to_emailID_list = cust_data['email']
			email_send_status = email_user_send_module(to_emailID_list,send_data)
		else:
			pass



def otp_generator():
	import random
	a = random.randint(1000,9999)
	return a