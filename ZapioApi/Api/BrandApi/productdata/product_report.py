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
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ZapioApi.Api.paginate import pagination
import math  
from UserRole.models import ManagerProfile
import dateutil.parser
from django.db.models import Count, Sum, Max, Avg, Case, When, Value, IntegerField, BooleanField
from ZapioApi.api_packages import *
from urbanpiper.models import *



class ProductReport(APIView):
	"""
	Product Report  POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for product report for brand.

		Data Post: {
			"start_date"            : "2019-07-24 00:00:00:00",
			"end_date"              : "2019-07-29 00:00:00:00",
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
			data = request.data
			err_message = {}
			s_date = data['start_date']
			e_date = data['end_date']
			try:
				start_date = dateutil.parser.parse(s_date)
				end_date = dateutil.parser.parse(e_date)
				if start_date < end_date:
					pass
				else:
					err_message["date"] = "Please provide meaning full date range!!"
			except Exception as e:
				err_message["date"] = "Please provide meaning full date range!!"
			if len(data["outlet_id"]) == 0:
				err_message["outlet"] = "Please select at least one outlet!!"
			else:
				for i in data["outlet_id"]:
					try:
						i = int(i)
					except Exception as e:
						err_message["outlet"] = "Outlet is not valid!!"
						break
			if any(err_message.values())==True:
					return Response({
						"success"	: 	False,
						"error" 	: 	err_message,
						"message" 	: 	"Please correct listed errors!!"
						})
			user = request.user.id
			orderdata = \
			Order.objects.filter(Q(order_time__lte=end_date),\
				Q(order_time__gte=start_date)).order_by('-order_time')
			outlet = data['outlet_id']
			ord_data =[]    
			for k in outlet:
				d = orderdata.filter(outlet_id=k)
				q_count = d.count()
				if q_count > 0: 
					for i in d:
						p_list ={}
						add = i.address
						p_list['id'] = i.id
						p_list['product_detail'] = []
						if i.is_aggregator == True:
							if i.order_description !=None:
								for j in i.order_description:
									alls = {}
									alls['order_id'] = i.outlet_order_id
									if 'name' in j:
										alls['name'] = j['name']
									if 'product_id' in j:
										sp = ProductSync.objects.filter(id = j['product_id'])
										if sp.count() > 0:
											pid =sp[0].product_id
											alls['id'] = j['product_id']
										else:
											pass
									else:
										pass
									if 'final_product_id' in j:
										alls['id'] = j['final_product_id']
									else:
										pass
									alls['price'] = j['price']
									if 'quantity' in j:
										alls['qty'] = j['quantity']
									else:
										alls['qty'] = 0
									alls['outlet'] = OutletProfile.objects.filter(id=i.outlet_id)[0].Outletname
									if 'food_type' in j:
										alls['food_type'] = j['food_type']
									ord_data.append(alls)
							else:
								pass
						else:
							if i.order_description !=None:
								for j in i.order_description:
									alls = {}
									alls['order_id'] = i.outlet_order_id
									if 'name' in j:
										alls['name'] = j['name']
									if 'product_id' in j:
										pid  = j['product_id']
									else:
										pass
									if 'id' in j:
										pid  = j['id']
									else:
										pass
									alls['price'] = j['price']
									if 'quantity' in j:
										alls['qty'] = j['quantity']
									else:
										alls['qty'] = 0
									alls['outlet'] = OutletProfile.objects.filter(id=i.outlet_id)[0].Outletname
									if 'food_type' in j:
										alls['food_type'] = j['food_type']
									else:
										alls['food_type'] = ''

									if 'varients' in j:
										if type(j['varients']) == str:
											alls['varients'] = j['varients']
										else:
											v = Variant.objects.filter(id=j['varients'])
											if v.count() > 0:
												alls['varients'] = v[0].variant
												alls['vid'] = v[0].id

											else:
												alls['varients'] = ''
									else:
										alls['varients'] = ''
										alls['vid'] = ''
									if 'size' in j:
										alls['varients'] = j['size']
										if j['size'] !='N/A':
											v = Variant.objects.filter(variant=j['size'])
											if v.count() > 0:
												alls['vid'] = v[0].id
											else:
												alls['vid'] = ''
									else:
										alls['varients'] = ''
										alls['vid'] = ''
									if alls['vid'] !='':
										sp = ProductSync.objects.filter(product_id = pid,variant_id=alls['vid'])
										if sp.count() > 0:
											alls['id'] = sp[0].id
										else:
											alls['id'] =''
									else:
										sp = ProductSync.objects.filter(product_id = pid)
										if sp.count() > 0:
											alls['id'] = sp[0].id
										else:
											alls['id'] =''
									ord_data.append(alls)
							else:
								pass
				else:
					pass
			if len(ord_data) > 0:
				return Response({"status":True,
								"orderdata":ord_data,
							})
			else:
				return Response({"status":True,
								"orderdata":[],
							   })
		except Exception as e:
			print(e)
			return Response(
						{"error":str(e)}
						)




