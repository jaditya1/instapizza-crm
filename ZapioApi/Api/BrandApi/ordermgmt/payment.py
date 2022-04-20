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
from django.db.models import Count, Sum, Max, Avg, Case, When, Value, IntegerField, BooleanField
from ZapioApi.api_packages import *


class PaymentReport(APIView):
	"""
	Order data GET API

		Authentication Required		: Yes
		Service Usage & Description	: .Download Order csv file

		Data Post: {
			"start_date" :""
			"end_date" : ""
			"outlet_id" : []
		}

		Response: {

			"success": True, 
			"message": "Dashboard card analysis api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
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
			outlet = data['outlet_id']
			orderdata = []
			que = Order.objects.filter(Q(order_time__lte=end_date),Q(order_time__gte=start_date),\
									Q(Company=cid)).distinct('outlet')
			
			orderdata = []
			for j in outlet:
				query = que.filter(outlet_id=j)
				if query.count() > 0:
					for i in query:
						adata = {}
						cname = Company.objects.filter(id=cid)[0].company_name
						adata['outlet_id'] = i.outlet_id
						adata['id'] = i.id
						if i.outlet_id != None:
							outlet_name = OutletProfile.objects.filter(id=i.outlet_id)[0].Outletname
							adata['outlet_name'] = str(cname)+' '+str(outlet_name)
						else:
							pass
					
						pdetail = Order.objects.filter(Q(order_time__lte=end_date),\
														Q(order_time__gte=start_date),\
														Q(Company=cid),\
														Q(outlet_id=i.outlet_id))
						
						adata['cod'] = 0
						adata['cod_count'] = 0
						adata['Dineout'] = 0
						adata['Dineout_count'] = 0
						adata['Paytm'] = 0
						adata['Paytm_count'] = 0
						adata['Razorpay'] = 0
						adata['Razorpay_count'] = 0
						adata['PayU'] = 0
						adata['PayU_count'] = 0
						adata['EDC'] = 0
						adata['EDC_count'] = 0
						adata['Mobiquik'] =0
						adata['Mobiquik_count'] =0
						adata['mix'] =0
						adata['Amex'] =0
						adata['Amex_count'] =0
						adata['yes'] =0
						adata['yes_count'] =0
						adata['total_amount'] =0
						adata['order_count'] =0
						for j in pdetail:
							if j.settlement_details !=None:
								if len(j.settlement_details) > 0:
									k = 1
									for k in j.settlement_details:
										if k['mode'] == 0:
											c = k['amount']
											adata['cod'] = adata['cod'] + float(c)
											adata['cod_count'] = adata['cod_count'] + 1
										else:
											pass
										if k['mode'] == 1:
											d = k['amount']
											adata['Dineout'] = adata['Dineout'] + float(d)
											adata['Dineout_count'] = adata['Dineout_count'] + 1
										else:
											pass
										if k['mode'] == 2:
											p = k['amount']
											adata['Paytm'] = adata['Paytm'] + float(p)
											adata['Paytm_count'] = adata['Paytm_count'] + 1
										else:
											pass
										if k['mode'] == 3:
											r = k['amount']
											adata['Razorpay'] = adata['Razorpay'] + float(r)
											adata['Razorpay_count'] = adata['Razorpay_count'] + 1
										else:
											pass
										if k['mode'] == 4:
											p = k['amount']
											adata['PayU'] = adata['PayU'] + float(p)
											adata['PayU_count'] = adata['PayU_count'] + 1
										else:
											pass
										if k['mode'] == 5:
											e = k['amount']
											adata['EDC'] = adata['EDC'] + float(e)
											adata['EDC_count'] = adata['EDC_count'] + 1
										else:
											pass
										if k['mode'] == 6:
											m = k['amount'] 
											adata['Mobiquik'] = adata['Mobiquik'] + float(m)
											adata['Mobiquik_count'] = adata['Mobiquik_count'] + 1
										else:
											pass
										if k['mode'] == 7:
											mix = k['amount']
										else:
											pass
										if k['mode'] == 8:
											a = k['amount']
											adata['Amex'] = adata['Amex'] + float(a)
											adata['Amex_count'] = adata['Amex_count'] + 1
										else:
											pass
										if k['mode'] == 9:
											y = k['amount']
											adata['yes'] = 	adata['yes'] + float(y)
											adata['yes_count'] = adata['yes_count'] + 1
										else:
											pass
									adata['total_amount'] = adata['Razorpay']+ \
															adata['Paytm'] +\
															adata['cod']+\
															adata['EDC']+\
															adata['Dineout']+\
															adata['PayU'] +\
															adata['yes'] + \
															adata['Amex'] + \
															adata['Mobiquik']
									adata['order_count'] = adata['Razorpay_count']+ \
															adata['Paytm_count'] +\
															adata['cod_count']+\
															adata['EDC_count']+\
															adata['Dineout_count']+\
															adata['PayU_count'] +\
															adata['yes_count'] + \
															adata['Amex_count'] + \
															adata['Mobiquik_count']
						orderdata.append(adata)
				else:
					pass

			if len(orderdata) > 0:
				return Response({
							"success": True,
							"data" : orderdata
							})
			else:
				return Response({
							"success": True,
							"data" : []
							})

		except Exception as e:
			return Response(
						{"error":str(e)}
						)
			
