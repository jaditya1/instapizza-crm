from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ZapioApi.Api.BrandApi.profile.profile import CompanySerializer
from Brands.models import Company
import json
#Serializer for api
from rest_framework import serializers
from Product.models import Variant, FoodType, AddonDetails, Product, ProductsubCategory,\
FeatureProduct
from Orders.models import Order,OrderStatusType, OrderTracking
from rest_framework.authtoken.models import Token
from Location.models import CityMaster, AreaMaster
from Outlet.models import DeliveryBoy,OutletProfile
from OutletApi.Api.serializers.order_serializers import OrderSerializer
from django.db.models import Q
from datetime import datetime, timedelta
from UserRole.models import * 
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import RetrievalData
from urbanpiper.models import UrbanOrders
from zapio.settings import Media_Path

# li = ["Acknowledged", "Food Ready", "Dispatched", "Completed", "Cancelled"]

class OrderListingData(APIView):
	"""
	Order listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for providing listing all order of brand.
	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			user = request.user
			outlet_data = ManagerProfile.objects.filter(auth_user_id=user.id)[0]
			outlet = outlet_data.outlet
			co_id = outlet_data.Company_id
			now = datetime.now()
			today = now.date()
			time_24_hours_ago = now - timedelta(days=1)
			ord_data =[]
			orderdata = Order.objects.filter(Q(order_time__gte=time_24_hours_ago),\
							Q(outlet_id__in=outlet)).order_by('-order_time')
			for i in orderdata:
				p_list ={}
				add = i.address
				p_list['id'] = i.id
				p_list['compnay_name'] = i.Company.company_name
				if i.Company.company_logo != None and i.Company.company_logo != "":
					p_list['company_logo'] = Media_Path + str(i.Company.company_logo)
				else:
					p_list['company_logo'] = None
				p_list['urban_detail'] = {}
				if i.is_aggregator == True:
					p_list['urban_detail']['is_aggregator'] = True
					p_list['urban_detail']['urban_order_id'] = i.urban_order_id
					aggre_order_staus = i.Aggregator_order_status
					if aggre_order_staus == 'Acknowledged':
						p_list['urban_detail']['next_states'] = 'Food Ready'
					elif aggre_order_staus == 'Food Ready':
						p_list['urban_detail']['next_states'] = 'Dispatched'
					elif aggre_order_staus == 'Dispatched':
						p_list['urban_detail']['next_states'] = 'Completed'
					elif aggre_order_staus == 'Completed':
						p_list['urban_detail']['next_states'] = 'Completed'
					else:
						p_list['urban_detail']['next_states'] = 'Cancelled'
				else:
					p_list['urban_detail']['is_aggregator'] = False
					p_list['urban_detail']['urban_order_id'] = "N/A"
					p_list['urban_detail']['next_states'] = "N/A"
				p_list['delivery_address'] = i.address
				p_list['special_instructions'] = i.special_instructions
				p_list['customer'] = i.customer
				p_list["Aggregator_order_status"] = i.Aggregator_order_status
				p_list['order_id'] = i.outlet_order_id
				p_list['order_status'] = i.order_status_id
				p_list['delivery_type'] = i.delivery_type

				p_list['discount_value'] = i.discount_value
				p_list['sub_total'] = i.sub_total
				p_list['total_bill_value'] = i.total_bill_value
				p_list['tax'] = i.taxes
				p_list['urban_order_id'] = i.urban_order_id
				p_list['channel_order_id'] = i.channel_order_id
				p_list['source'] = i.order_source
				o_time = i.order_time+timedelta(hours=5,minutes=30)
				p_list['order_time'] = o_time.strftime("%d/%b/%y %I:%M %p")
				p_list['delivery_time'] = i.delivery_time
				if p_list['delivery_time'] != None:
					d_time = i.delivery_time+timedelta(hours=5,minutes=30)
					p_list['delivery_time'] = d_time.strftime("%d/%b/%y %I:%M %p")
				else:
					p_list['delivery_time'] = None
				if i.settlement_details !=None:
					if len(i.settlement_details) > 0:
						for k in i.settlement_details:
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
								if k['mode'] == 16:
									p_list['payment_mode'] = "Magic Pin"
							else:
								if i.is_aggregator == True:
									p_list['payment_mode'] = i.aggregator_payment_mode
								else:
									p_list['payment_mode'] = ''
					else:
						if i.is_aggregator == True:
							p_list['payment_mode'] = i.aggregator_payment_mode
						else:
							p_list['payment_mode'] = ''
				else:
					if i.is_aggregator == True:
						p_list['payment_mode'] = i.aggregator_payment_mode
					else:
						p_list['payment_mode'] = ''

				if i.is_aggregator == False:
					order_status_rec = OrderStatusType.objects.filter(id=i.order_status_id)
					if order_status_rec.count() != 0:
						p_list['order_status_name'] =\
						order_status_rec.first().Order_staus_name
						p_list['color_code'] = order_status_rec.first().color_code
					else:
						return Response(
							{"message":"Order Status Configuration data is not set in backend!!"})
				else:
					p_list['order_status_name'] = i.Aggregator_order_status
				p_list["can_process"] = True

				if i.order_status.can_process == 1:
					pass
				else:
					p_list["can_process"] = False
				if i.outlet != None:
					p_list["outlet_name"] = i.outlet.Outletname
					p_list["outlet_id"] = i.outlet_id
				else:
					p_list["outlet_name"] ='N/A'

				p_list["is_rider_assign"]  = i.is_rider_assign
				p_list["rider_detail"] = [] 
				if i.is_rider_assign == True:
					if i.is_aggregator == False:
						a = {}
						ad = DeliveryBoy.objects.filter(id=i.delivery_boy_id)
						a['name'] = ad[0].name
						a['email'] = ad[0].email
						a['mobile'] = ad[0].mobile
						p_list["rider_detail"].append(a)
					else:
						rider_detail = i.delivery_boy_details
						p_list["rider_detail"].append(rider_detail)
				else:
					a = {}
					a['name'] = ''
					a['email'] = ''
					a['mobile'] = ''
					p_list["rider_detail"].append(a)
				ord_data.append(p_list)
			return Response({"status":True,
							"orderdata":ord_data})
		except Exception as e:
			return Response(
						{"error":str(e)}
						)






