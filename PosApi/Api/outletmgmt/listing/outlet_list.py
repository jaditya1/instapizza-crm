from rest_framework.views import APIView
from rest_framework.response import Response
from Brands.models import Company
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import re
from datetime import datetime
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import os
from rest_framework import serializers
from Outlet.models import OutletProfile
from UserRole.models import * 
from urbanpiper.models import OutletSync, ProductSync
from Orders.models import Order
from django.db.models import Q
from django.db.models import Count, Sum, Max, Avg, Case, When, Value, IntegerField, BooleanField
from History.models import OutletLogs
from datetime import datetime, timedelta

class AllOutlet(APIView):

	"""
	All Outlet list GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of outlet within brand

	"""

	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			user = request.user
			co_id = ManagerProfile.objects.filter(auth_user_id=user.id)[0].Company_id
			outlet_data = ManagerProfile.objects.filter(auth_user_id=user.id)
			outlet = outlet_data[0].outlet
			final_result = []
			now = datetime.now()
			month = now.month
			year = now.year
			if outlet != None:
				for j in outlet:
					record = OutletProfile.objects.filter(id=j,active_status=1)
					if record.count() > 0:
						for i in record:
							q_dict = {}
							urban_record = OutletSync.objects.filter(outlet=i.id,sync_status='synced')
							if urban_record.count() == 0:
								q_dict["is_urban_synced"] = False
							else:
								q_dict["is_urban_synced"] = True
							menu_synced_record = \
							ProductSync.objects.filter(outlet_map__contains=[str(i.id)])
							if menu_synced_record.count() != 0:
								q_dict["is_menu_synced"] = True
							else:
								q_dict["is_menu_synced"] = False
							q_dict["id"] = i.id
							q_dict["Outletname"] = i.Outletname

							ol = OutletLogs.objects.filter(outlet=i.id)
							if ol.count() > 0:
								if ol.last().opening_time !=None:
									o_time = ol.last().opening_time+timedelta(hours=5,minutes=30)
									ot = str(o_time.time())
									s = ot.split('.')
									q_dict["opening_time"] = s[0]
								if ol.last().closing_time !=None:
									c_time = ol.last().closing_time+timedelta(hours=5,minutes=30)
									ct = str(c_time.time())
									c = ct.split('.')
									q_dict["closing_time"] = c[0]
							else:
								q_dict["opening_time"] = ''
								q_dict["closing_time"] = ''

							q_dict["is_pos_open"] = i.is_pos_open
							order_record = Order.objects.filter(Q(outlet_id=i.id),Q(order_status=6))
							c = order_record.filter(order_time__year=year,\
								order_time__month=month)
							order_result = order_record.values('Company').\
							annotate(total_revenue=Sum('total_bill_value'),order_count=Count("id"))
							if len(order_result) > 0:
								q_dict["total_sale"] = order_result[0]["total_revenue"]
								q_dict["total_order"] = order_result[0]["order_count"]
							else:
								q_dict["total_sale"] = 0
								q_dict["total_order"] = 0
							q_dict["company_id"] = i.Company_id
							final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "Outlet Listing api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Outlet listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})

