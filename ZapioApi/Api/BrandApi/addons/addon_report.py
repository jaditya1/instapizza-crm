from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
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
import math  
from UserRole.models import ManagerProfile
import dateutil.parser
from django.db.models import Count, Sum, Max, Avg, Case, When, Value, IntegerField, BooleanField
from ZapioApi.api_packages import *



class AddonReport(APIView):
	"""
	Addon Report  POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for addon report for brand.

		Data Post: {
			"start_date"            : "2019-07-24 00:00:00:00",
			"end_date"              : "2019-07-29 00:00:00:00" ,
			"outlet_id"             : []                           
		}

		Response: {

			"success": True, 
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			mutable = request.POST._mutable

			request.POST._mutable = True
			data = request.data
			err_message = {}
			if data["start_date"] != '' and data["end_date"] != '':
				start_date = dateutil.parser.parse(data["start_date"])
				end_date = dateutil.parser.parse(data["end_date"])
				if start_date > end_date:
					err_message["from_till"] = "Validity dates are not valid!!"
			else:
				pass
			if len(data["outlet_id"]) > 0:
				outlet_unique_list = []
				for i in data["outlet_id"]:
					err_message["outlet_map"] = validation_master_anything(str(i),
												"Outlet",contact_re, 1)
					if err_message["outlet_map"] != None:
						break
					if i not in outlet_unique_list:
						outlet_unique_list.append(i)
					else:
						err_message["duplicate_outlet"] = "Outlet are duplicate!!"
						break
					record_check = OutletProfile.objects.filter(Q(id=i),Q(active_status=1))
					if record_check.count() == 0:
						err_message["outlet_map"] = "Outlet is not valid!!"
						break
					else:
						pass
			else:
				err_message["outlet_map"] = "Please Enter Outlet!!"

			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})

			user = request.user.id
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
				outlet = Company.objects.filter(auth_user_id=user)
				cid = outlet[0].id
			else:
				pass
			if data["start_date"] != '' and data["end_date"] != '':
				orderdata = Order.objects.filter(Q(order_time__lte=end_date),Q(order_time__gte=start_date)
					,Q(Company=cid)).order_by('-order_time')
			else:
				pass
			outlet = data['outlet_id']
			ord_data =[]  
			ord_data1 =[]  
			ord_data3 = []
			for k in outlet:
				d = orderdata.filter(outlet_id=k)
				q_count = d.count()
				if q_count > 0:
					for i in d:
						if i.is_aggregator==True:
							if i.order_description !=None:
								for j in i.order_description:
									if 'add_ons' in j:
										k = j['add_ons']
										for p in k:
											alls = {}
											price = p['price']
											if 'addon_name' in p:
												alls['addon_name']  = p['addon_name']
											else:
												pass
											if 'title' in p:
												alls['addon_name']  = p['title']
											else:
												pass	
											if 'quantity' in p:
												alls['quantity']  = p['quantity']
											else:
												alls['quantity']  = j['quantity']											
											alls['order_id'] = i.outlet_order_id
											alls['price'] = p['price']
											alls['source'] = i.payment_source
											o = i.order_time
											o_time = o+timedelta(hours=5,minutes=30)
											alls['time'] = str(o_time.strftime("%I:%M %p"))
											alls['dt'] = str(o_time.strftime("%d/%b/%y"))
											alls['outlet'] =  \
											OutletProfile.objects.\
											filter(id=i.outlet_id)[0].Outletname
		
											ord_data.append(alls)
									else:
										pass
							else:
								pass
						else:
							if i.order_description !=None:
								for j in i.order_description:
									if 'add_ons' in j:
										k = j['add_ons']
										for p in k:
											alls = {}
											price = p['price']
											if 'addon_name' in p:
												alls['addon_name']  = p['addon_name']
											else:
												pass
											if 'title' in p:
												alls['addon_name']  = p['title']
											else:
												pass
											if 'quantity' in p:
												alls['quantity']  = p['quantity']
											else:
												alls['quantity'] = 1	
											alls['order_id'] = i.outlet_order_id
											alls['price'] = p['price']
											alls['source'] = i.payment_source
											o = i.order_time
											o_time = o+timedelta(hours=5,minutes=30)
											alls['time'] = str(o_time.strftime("%I:%M %p"))
											alls['dt'] = str(o_time.strftime("%d/%b/%y"))
											alls['outlet'] =  OutletProfile.objects.filter(id=i.outlet_id)[0].Outletname
											ord_data1.append(alls)
									else:
										pass
							else:
								pass
				else:
					pass


			ord_data3 = ord_data + ord_data1

			if len(ord_data3) > 0:
				return Response({"status":True,
								"orderdata":ord_data3,
							})
			else:
				return Response({"status":True,
								"orderdata":[],
							   })
		except Exception as e:
			return Response(
						{"error":str(e)}
						)


