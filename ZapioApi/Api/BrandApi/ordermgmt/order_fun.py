from rest_framework.views import APIView
from rest_framework.response import Response
from ZapioApi.api_packages import *
from datetime import datetime, timedelta
from Orders.models import Order,OrderStatusType,OrderTracking
from Product.models import Product
from OutletApi.Api.serializers.order_serializers import BoySerializer,OrderTrackSerializer, \
OrderSerializer
from urbanpiper.models import UrbanOrders
from ZapioApi.Api.urbanpiper.sync.order_status_update import Order_status_update
from Outlet.models import DeliveryBoy,OutletProfile, TempTracking
from UserRole.models import *
from Brands.models import Company
from zapio.settings import Media_Path
from Dunzo.models import Unprocessed_Order_Quote, Processed_Order_Quote

li = ["Acknowledged", "Food Ready", "Dispatched", "Completed", "Cancelled"]

def urban_order(order_data):
	urban_order_id = order_data.urban_order_id
	urban_record = UrbanOrders.objects.filter(order_id=urban_order_id)
	if urban_record.count() == 0:
		return False
	else:
		q = urban_record[0]
		next_states = q.next_states
		current_state = q.order_state
		if current_state == "Food Ready":
			return "cannot_process"
		else:
			pass
		if current_state not in next_states:
			status_change = next_states[0]
		elif current_state != "Dispatched" and current_state != "Completed" and current_state != "Cancelled":
			status_change = "Food Ready"
		elif current_state == "Cancelled":
			return "aggregator_cancelled"
		else:
			return "cannot_process"
		sync_order = Order_status_update(urban_order_id, status_change)
		if sync_order == None:
			return False
		else:
			return "processed"


def ChangestatusData(data):
	uid = data['user']
	user_data = ManagerProfile.objects.filter(auth_user_id=uid)
	key_person = user_data[0].username
	err_message = {}
	order_track = {}
	dboy = {}
	order_dict = {}
	err_message["order_id"] = \
			validation_master_anything(data["order_id"],
			"Order Id",contact_re, 1)
	if any(err_message.values())==True:
		err ={
			"success": False,
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			}
		return err
	order_record = Order.objects.filter(id=data['order_id'])
	order_data = order_record.first()
	urban_order_id = order_data.urban_order_id
	if order_data.is_aggregator == True:
		urban_process = urban_order(order_data)
		if urban_process == False:
			err = {
			"success" : False,
			"message" : "Order can'nt be processed..something went wrong while"\
						" communicating with third party services!!"
			}
			return err
		elif urban_process == "cannot_process":
			err = {
			"success" : False,
			"message" : "Order is already processed!!"
			}
			return err
		else:
			pass
	else:
		pass
	updated_order = Order.objects.filter(urban_order_id=urban_order_id)
	Aggregator_order_status = updated_order[0].Aggregator_order_status
	order_status_id = order_data.order_status_id
	order_priority = order_data.order_status.priority
	order_status_record = OrderStatusType.objects.filter(id__gt=order_status_id,\
			priority__gt=order_priority,active_status=1).order_by('priority')
	if order_status_record.count()==0:
		err_message = {}
		err_message["change_status"] = "Order is already processed!!"
		err = {
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			}
		return err
	else:
		if order_data.is_aggregator == False:
			order_dict["order_status"] = order_status_record[0].id
			is_delivered_rec = OrderStatusType.objects.filter(id=order_dict["order_status"])
			if is_delivered_rec[0].Order_staus_name == "Delivered":
				order_dict["delivery_time"] = datetime.now()
				order_dict["is_completed"] = 1
			else:
				pass
			order_dict["Aggregator_order_status"] = Aggregator_order_status
			a = ManagerProfile.objects.filter(auth_user_id=data['user'])
			order_dict["user"] = a[0].username
			Order_serializer = OrderSerializer(order_data,data=order_dict,partial=True)
			if Order_serializer.is_valid():
				s=Order_serializer.save()
				order_track["order"] = data['order_id']
				order_track["Order_staus_name"] = order_dict['order_status']
				order_track["key_person"] = key_person
				Order_track_serializer = OrderTrackSerializer(data=order_track)
				if Order_track_serializer.is_valid():
					Order_track_serializer.save()
				else:
					err = {
							"success": False, 
							"message" : Order_track_serializer.errors,
							}
					return err
			else:
				err = {
						"success": False, 
						"message" : Order_serializer.errors,
					  }
			err = {
					"success": True, 
					"message" : "Order Status changed successfully!!",
				 }
		else:
			err = {
					"success": True, 
					"message" : "Order Status changed successfully!!",
				 }
		return err

def RetrievalData(data):
	data["id"] = str(data["id"])
	err_message = {}
	err_message["id"] = \
			validation_master_anything(data["id"],
			"Order Id",contact_re, 1)
	if any(err_message.values())==True:
		err = {
			"success": False,
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			}
		return err
	order_record = Order.objects.filter(id=data['id'])
	if order_record.count() == 0:
		err = {
			    "success": False,
				"message": "Required Order data is not valid to retrieve!!"
		}
		return err
	else:
		final_result = []
		p_list = {}
		p_list["id"] = order_record[0].id
		add = order_record[0].address
		p_list['order_id'] = order_record[0].order_id
		p_list["log"] = []
		orderlog = OrderTracking.objects.filter(order_id=p_list["id"]).order_by('id')
		if orderlog.count() > 0:
			for j in orderlog:
				r_list ={}
				r_list['id'] = j.id
				r_list['status_name'] = j.Order_staus_name.Order_staus_name
				created_at = j.created_at+timedelta(hours=5,minutes=30)
				r_list["created_at"] = created_at.strftime("%d/%b/%y %I:%M %p")
				r_list['key_person'] = j.key_person
				p_list["log"].append(r_list)
		else:
			pass
		if add == None:
			pass
		else:
			if 'longitude' in add:
				p_list['longitude'] = add['longitude']
			else:
				p_list['longitude'] = ''
			if 'latitude' in add:
				p_list['latitude'] = add['latitude']
			else:
				p_list['latitude'] = ''
		p_list['address'] = order_record[0].address
		p_list['order_status'] = order_record[0].order_status_id
		p_list['is_aggregator'] = order_record[0].is_aggregator
		p_list['order_type'] = order_record[0].order_type
		if order_record[0].order_source == None:
			p_list['source'] = "Website"
		else:
			p_list['source'] = order_record[0].order_source
	
		if order_record[0].settlement_details !=None:
			if len(order_record[0].settlement_details) > 0:
				for k in order_record[0].settlement_details:
					if k['mode'] !=None:
						if k['mode'] == 0:
							p_list['payment_mode'] = "Cash on Delivery"
						else:
							pass
						if k['mode'] == 1:
							p_list['payment_mode'] = "Dineout"
						else:
							pass
						if k['mode'] == 2:
							p_list['payment_mode'] = "Paytm"
						else:
							pass
						if k['mode'] == 3:
							p_list['payment_mode'] = "Razorpay"
						else:
							pass
						if k['mode'] == 4:
							p_list['payment_mode'] = "PayU"
						else:
							pass
						if k['mode'] == 5:
							p_list['payment_mode'] = "EDC"
						else:
							pass
						if k['mode'] == 6:
							p_list['payment_mode'] = "Mobiquik"
						else:
							pass
						if k['mode'] == 7:
							p_list['payment_mode'] = "Mix"
						else:
							pass
						if k['mode'] == 8:
							p_list['payment_mode'] = "EDC Amex"
						else:
							pass
						if k['mode'] == 9:
							p_list['payment_mode'] = "EDC Yes Bank"
						else:
							pass
						if k['mode'] == 10:
							p_list['payment_mode'] = "Swiggy"
						else:
							pass
						if k['mode'] == 11:
							p_list['payment_mode'] = "Z Prepaid"
						else:
							pass
						if k['mode'] == 12:
							p_list['payment_mode'] = "S Prepaid"
						else:
							pass
						if k['mode'] == 13:
							p_list['payment_mode'] = "Dunzo"
						else:
							pass
						if k['mode'] == 14:
							p_list['payment_mode'] = "Zomato Cash"
						else:
							pass
						if k['mode'] == 15:
							p_list['payment_mode'] = "Zomato"
						else:
							pass
					else:
						if order_record[0].is_aggregator == True:
							p_list['payment_mode'] = order_record[0].aggregator_payment_mode
						else:
							p_list['payment_mode'] =''
			else:
				if order_record[0].is_aggregator == True:
					p_list['payment_mode'] = order_record[0].aggregator_payment_mode
				else:
					p_list['payment_mode'] =''
		else:
			if order_record[0].is_aggregator == True:
				p_list['payment_mode'] = order_record[0].aggregator_payment_mode
			else:
				p_list['payment_mode'] =''
		if order_record[0].is_aggregator == False:
			p_list['order_status_name'] = \
			OrderStatusType.objects.filter(id=order_record[0].order_status_id).first().Order_staus_name
			p_list['color_code'] = \
			OrderStatusType.objects.filter(id=order_record[0].order_status_id).first().color_code
		else:
			p_list['order_status_name'] = order_record[0].Aggregator_order_status
		cus = order_record[0].customer
		if cus !='':
			p_list['name'] = cus['name']
			if "email" in cus:
				p_list['email'] = cus['email']
			else:
				pass
			if "mobile_number" in cus:
				p_list['mobile'] = cus['mobile_number']
				
			if "mobile" in cus:
				p_list['mobile'] = cus['mobile']
		else:
			pass
		p_list['order_description'] = order_record[0].order_description
		if order_record[0].is_aggregator == False:
			for i in p_list['order_description']:
				if "id" in i:
					p_id = i["id"]
					i["food_type"] = \
						Product.objects.filter(id=p_id)[0].food_type.food_type
				else:
					pass
		else:
			pass
			
		from generic_services.order_kot import kot_process_data
		final_order_description = kot_process_data(data["id"])
		p_list['order_description'] = final_order_description
		o_time = order_record[0].order_time+timedelta(hours=5,minutes=30)
		p_list['order_time'] = o_time.strftime("%d/%b/%y %I:%M %p")
		if order_record[0].delivery_time != None:
			d_time = order_record[0].delivery_time+timedelta(hours=5,minutes=30)
			p_list['delivery_time'] = d_time.strftime("%d/%b/%y %I:%M %p")
		else:
			p_list['delivery_time'] = None
		if order_record[0].external_discount != None:
			external_discount = order_record[0].external_discount
		else:
			external_discount = 0
		p_list['taxes'] = order_record[0].taxes
		p_list['sub_total'] = order_record[0].sub_total
		p_list['discount_value'] = order_record[0].discount_value
		p_list['total_bill_value'] = order_record[0].total_bill_value
		p_list['print_discount_value'] = \
		order_record[0].discount_value - external_discount
		p_list['print_total_bill_value'] = \
		(p_list['sub_total'] - p_list['print_discount_value']) + p_list['taxes']
		p_list['special_instructions'] = order_record[0].special_instructions
		p_list['company_logo'] = Media_Path+str(order_record[0].Company.company_logo)
		p_list["is_rider_assign"]  = order_record[0].is_rider_assign
		p_list["other_order_id"]  = order_record[0].outlet_order_id
		p_list["Aggregator_order_status"] = order_record[0].Aggregator_order_status
		p_list['urban_order_id'] = order_record[0].urban_order_id
		p_list['channel_order_id'] = order_record[0].channel_order_id
		p_list['cancel_reason'] = order_record[0].order_cancel_reason
		p_list['discount_name'] = order_record[0].discount_name
		p_list['cancel_responsibility'] = order_record[0].cancel_responsibility
		p_list["rider_detail"] = []
		rider_detail = order_record[0].delivery_boy_details 
		if order_record[0].is_rider_assign == True:
			if order_record[0].is_aggregator == False:
				a = {}
				ad = DeliveryBoy.objects.filter(id=order_record[0].delivery_boy_id)
				a['name'] = ad[0].name
				a['email'] = ad[0].email
				a['mobile'] = ad[0].mobile
				p_list["rider_detail"].append(a)
			else:
				p_list["rider_detail"].append(rider_detail)
		else:
			if rider_detail == None:
				a = {}
				a['name'] = ''
				a['email'] = ''
				a['mobile'] = ''
				p_list["rider_detail"].append(a)
			else:
				p_list["rider_detail"].append(rider_detail)
		p_list["temp_detail"] = []
		today = datetime.now().date()
		outlet_id = order_record[0].outlet_id
		temp_record = \
		TempTracking.objects.filter(outlet=outlet_id,created_at__date=today,is_latest=1).\
														order_by('-created_at')
		if temp_record.count() == 0:
			p_list['time_stamp'] = None
		else:
			for j in temp_record:
				data_dict = {}
				data_dict['staff_id'] = j.staff_id
				data_dict['staff_name'] = j.staff.manager_name
				data_dict['body_temp'] = j.body_temp
				data_dict['spo2'] = j.SPO2
				p_list["temp_detail"].append(data_dict)
			t = j.created_at+timedelta(hours=5,minutes=30)
			p_list["time_stamp"] = t.strftime("%Y-%m-%d %I:%M %p")
		p_list["Outletname"] = order_record[0].outlet.Outletname
		p_list["outlet_address"] = order_record[0].outlet.address
		p_list["dunzo_quote_details"] = []
		quote_data = Processed_Order_Quote.objects.filter(order_quote_id=data["id"])
		quote_dict = {}
		if quote_data.count()!=0:
			q_row =  quote_data[0]
			quote_dict["distance"] = str(q_row.distance)+"	kms"
			quote_dict["estimated_price"] = q_row.estimated_price
			quote_dict["estimated_time"] = q_row.eta
		else:
			quote_dict["distance"] = "N/A"
			quote_dict["estimated_price"] = "N/A"
			quote_dict["estimated_time"] = {"pickup":"N/A","dropoff":"N/A"}
		p_list["dunzo_quote_details"].append(quote_dict)
		p_list["company_name"] = order_record[0].Company.company_name
		final_result.append(p_list)
		err = {
				"success": True, 
				"message": "Order data retrieval api worked well!!",
				"data": final_result,
				}
	return err


def get_user(user):
	is_outlet = OutletProfile.objects.filter(auth_user_id=user)
	is_brand = Company.objects.filter(auth_user_id=user)
	is_cashier = ManagerProfile.objects.filter(auth_user_id=user)
	if is_cashier.count() > 0:
		cid = ManagerProfile.objects.filter(auth_user_id=user)[0].Company_id
	else:
		pass
	if is_outlet.count() > 0:
		outlet = OutletProfile.objects.filter(auth_user_id=user)
		cid = outlet[0].Company_id
	else:
		pass
	if is_brand.count() > 0:
		brand = Company.objects.filter(auth_user_id=user)
		cid = brand[0].id
	else:
		pass
	return cid
