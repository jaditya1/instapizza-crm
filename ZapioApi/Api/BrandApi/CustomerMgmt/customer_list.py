from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Brands.models import Company
import json
#Serializer for api
from rest_framework import serializers
from django.db.models import Q
from datetime import datetime, timedelta
from Customers.models import CustomerProfile
from Orders.models import Order
from django.db.models import Sum,Count,Max
from Outlet.models import OutletProfile
from ZapioApi.Api.paginate import pagination
import math  
from UserRole.models import ManagerProfile
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from rest_framework_tracking.mixins import LoggingMixin

def order_analysis(q):
	record = \
	Order.objects.filter(Company_id=q["company_id"],customer__mobile_number=q["mobile"])
	first_order = record[0].order_time
	last_order = record.last().order_time
	q["total_order"] = record.count()
	full_addr = record.last().address
	q["address"] = full_addr["address"]
	total_spent = record.aggregate(Sum('total_bill_value'))
	q["total_spent"] = total_spent['total_bill_value__sum']
	q_pre_outlet = record.values('outlet').annotate(visit_count=Count('outlet'))
	visited_outlet = {}
	for i in q_pre_outlet:
		visited_outlet[i["outlet"]] = i["visit_count"]
	outlet_id = max(visited_outlet, key=visited_outlet.get) 
	q["preferred_outlet"] = OutletProfile.objects.filter(id=outlet_id)[0].Outletname
	day_diff = (last_order.date()-first_order.date()).days
	if record[0].has_been_here == 0:
		q["customer_type"] = "New"
	else:
		q["customer_type"] = "Loyal"
	return q

class UserlistingSearch(LoggingMixin,APIView):

	"""
	Customer listing and Search POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for providing the profile details of 
		customers based on searched key or all customers.

		Data Post: {
		
			"search_key"                   : 		"adi"(Optional Key)

		}

		Response: {

			"status"		:	True,
			"data"			:	final_result,
			"page_count"	:	page_count
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			user = self.request.user.id
			data = request.data
			allcustomer = \
			CustomerProfile.objects.filter(Q(company=1)|Q(company=5)|Q(company=6))
			if "search_key" in data:
				key = data["search_key"]
				if key != "" and key != None:
					allcustomer = \
					allcustomer.filter(Q(name__icontains=key)|Q(mobile__icontains=key))
				else:
					pass
			else:
				pass
			allcustomer = allcustomer.order_by('-created_at')
			q_count = allcustomer.count()
			page_count = math.ceil((q_count/20))
			page = request.GET.get('page', 1)
			paged_query = pagination(allcustomer,page)
			final_result = []
			for i in paged_query:
				q_dict = {}
				q_dict["id"] = i.id
				q_dict["company_id"] = i.company_id
				q_dict["name"] = i.name
				q_dict["email"] = i.email
				q_dict["mobile"] = i.mobile
				q_dict['created_at'] = i.created_at.strftime("%d/%b/%y")
				aa = Order.objects.filter(Company_id=q_dict["company_id"],\
					                customer__mobile_number=q_dict["mobile"])
				if aa.count() > 0:
					order_pattern = order_analysis(q_dict)
				else:
					q_dict["total_order"] = "N/A"
					q_dict["total_spent"] = "N/A"
					q_dict["customer_type"] = "New"
					order_pattern = q_dict
				final_result.append(order_pattern)
			return Response({
							"status"		:	True,
							"data"			:	final_result,
							"page_count"	:	page_count
							})
		except Exception as e:
			return Response({
					"error"	:	str(e)
						})



