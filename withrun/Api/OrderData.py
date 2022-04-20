from datetime import datetime
import requests
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework import serializers
from django.http import HttpResponse
from Orders.models import Order,OrderStatusType,OrderTracking
from rest_framework.permissions import IsAuthenticated
import dateutil.parser
from Brands.models import Company
from Outlet.models import OutletProfile
from rest_framework.authtoken.models import Token
from UserRole.models import ManagerProfile
from datetime import datetime, timedelta
import secrets
from urbanpiper.models import ProductSync
from Product.models import Addons
from withrun.models import *


def order_structure(order_data, is_aggregator):
	if is_aggregator == True:
		for i in order_data:
			i['unit_price'] = i['price']/i['quantity']
			add_on_price = 0
			for j in i['add_ons']:
				add_on_price = add_on_price + j['price']
				j['addon_qty'] = i["quantity"]
			i['unit_price'] =  i['unit_price'] - add_on_price
	else:
		for i in order_data:
			try:
				i['unit_price'] = int(i['price'])
			except Exception as e:
				i['unit_price'] = 0
			sync_record = ProductSync.objects.filter(product=i['id'])
			if i['size'] != "N/A" and i["size"] != "":
				sync_record = sync_record.filter(variant__variant=i['size'])
			else:
				pass
			if sync_record.count() == 0:
				i['final_product_id'] = "N/A"
			else:
				i['final_product_id'] = sync_record[0].id
			add_on_price = 0
			for j in i['add_ons']:
				add_on_price = add_on_price + j['price']
				j['addon_qty'] = i["quantity"]
			i['unit_price'] =  i['unit_price'] - add_on_price
	return order_data


secret_token = "ac9e95c60497d701c2666490583d877c26c2519bb4a8ba3c990c5e82c4fabc4basinfuenvudh155weXOPio"

class OrdersDetail(APIView):
	"""
	Order data WithRun GET API

		Authentication Required		: Yes
		Service Usage & Description	: This service will be used to get order data.

		Data Post: {
		}

		Response: {

			"success": True, 
			"message": "Orders API worked well!!",
			"data": final_result
		}

	"""
	# permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		getdata = request.META
		if 'HTTP_TOKEN' in getdata:
			pass
		else:
			return Response({
				"success" : False,
				"message" : "Credentials Not provided!!"
				})
		token = getdata['HTTP_TOKEN']
		if token != secret_token:
			return Response({
				"success" : False,
				"message" : "Provided Credentials do'nt match!!"
				})
		else:
			pass
		limit = request.GET.get('__limit',None)
		order_by = request.GET.get('__order_by',None)
		shop_id = request.GET.get('__ref_shop_id',None)
		created_at = request.GET.get('__created_on_datetime__gte', None)
		created_at_lte = request.GET.get('__created_on_datetime__lte', None)
		if limit == None:
			pass
		else:
			try:
				limit = int(limit)
			except Exception as e:
				return Response({
				"success" : False,
				"message" : "Limit parameter is not valid!!"
				})
		if created_at == None:
			return Response({
				"success" : False,
				"message" : "Time is not provided!!"
				})
		else:
			try:
				created_at = dateutil.parser.parse(created_at)
				now = datetime.now().date()
				if created_at.date() > now:
					return Response({
						"success" : False,
						"message" : "Provide meaning full date!!"
						}) 
				else:
					pass
			except Exception as e:
				return Response({
						"success" : False,
						"message" : "Date format is not valid!!"
						}) 
		if shop_id == None:
			return Response({
				"success" : False,
				"message" : "Shop Id is not provided!!"
				})
		else:
			try:
				shop_id = int(shop_id)
			except Exception as e:
				return Response({
				"success" : False,
				"message" : "Shop Id is not valid!!"
				})	
		orderdata = Order.objects.filter(Q(outlet_id=shop_id),Q(order_time__gte=created_at)).\
																		order_by('-order_time')
		orderdata = orderdata.filter(Q(order_status=6)|Q(order_status=7))
		if created_at_lte == None:
			pass
		else:
			orderdata = orderdata.filter(Q(order_time__lte=created_at_lte))
		ord_data =[]
		for i in orderdata:
			synced_record = SyncOrders.objects.filter(order=i.id)
			if synced_record.count() == 0:
				synced_create = SyncOrders.objects.create(outlet_id=i.outlet_id,order_id=i.id)
			else:
				pass
			p_list ={}
			add = i.address
			p_list['id'] = i.id
			p_list['invoice_number'] = i.outlet_order_id
			p_list['order_status'] = i.order_status_id
			if p_list['order_status'] == 6:
				p_list['order_status_name'] = 'Completed'
			else:
				p_list['order_status_name'] = 'Cancelled'
			if i.external_discount != None:
				external_discount = i.external_discount
			else:
				external_discount = 0
			p_list['discount_value'] = (i.discount_value-external_discount)
			p_list['sub_total'] = i.sub_total
			p_list['total_tax'] = i.taxes
			p_list['total_bill_value'] = i.total_bill_value
			p_list['source'] = i.order_source
			o_time = i.order_time+timedelta(hours=5,minutes=30)
			p_list['order_time'] = o_time.strftime("%d/%b/%y %I:%M %p")
			p_list['delivery_time'] = i.delivery_time
			if p_list['delivery_time'] != None:
				d_time = i.delivery_time+timedelta(hours=5,minutes=30)
				p_list['delivery_time'] = d_time.strftime("%d/%b/%y %I:%M %p")
			else:
				p_list['delivery_time'] = None
			if  i.payment_mode == '0':
				p_list['payment_mode'] = "Cash on Delivery"
			else:
				p_list['payment_mode'] = "Online"
			order_detail = order_structure(i.order_description, i.is_aggregator)
			# order_detail = i.order_description
			p_list["items"] = order_detail
			p_list['delivery_address'] = i.address
			p_list['special_instructions'] = i.special_instructions
			p_list['customer'] = i.customer
			if i.outlet != None:
				p_list["outlet_name"] = i.outlet.Outletname
			else:
				p_list["outlet_name"] ='N/A'
			p_list['created_on'] = p_list['order_time']
			order_status_id = i.order_status_id

			order_track = \
			OrderTracking.objects.filter(order=i.id,Order_staus_name=3)
			if order_track.count() == 1:
				p_list["food_ready"] = "yes"
			else:
				p_list["food_ready"] = "no"
			ord_data.append(p_list)
		if orderdata.count() != 0:
			company_id = orderdata[0].Company_id
			outlet_id = orderdata[0].outlet_id
			sync_record = OrderSync.objects.filter(Company=company_id,outlet=outlet_id)
			if sync_record.count() == 1:
				sync_update = sync_record.update(last_synced=datetime.now())
			else:
				sync_create = OrderSync.objects.create(Company_id=company_id,outlet_id=outlet_id,\
										last_synced=datetime.now())
		else:
			pass
		return Response({
			"status"	:	True,
			"data"		:	ord_data
			})
		return Response({
			"success"	: 	True, 
			"message"	: 	"Orders API worked well!!",
			"data"   	: 	[]
			})
