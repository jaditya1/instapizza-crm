from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
from Orders.models import Order
from Customers.models import CustomerProfile
from django.db.models import Sum,Count,Max
from Outlet.models import OutletProfile

def order_analysis(q):
	record = \
	Order.objects.filter(Company_id=q["company_id"],customer__mobile_number=q["mobile"])
	first_order = record[0].order_time
	last_order = record.last().order_time
	q["first_order"] = first_order.strftime("%d/%b/%Y %I:%M %p")
	q["last_order"] = last_order.strftime("%d/%b/%Y %I:%M %p")
	q["total_order"] = record.count()
	full_addr = record.last().address
	q["address"] = full_addr["address"]
	total_spent = record.aggregate(Sum('total_bill_value'))
	q["total_spent"] = total_spent['total_bill_value__sum']
	q["order_avg"] = round(q["total_spent"]/q["total_order"],2)
	q_pre_outlet = record.values('outlet').annotate(visit_count=Count('outlet'))
	visited_outlet = {}
	for i in q_pre_outlet:
		visited_outlet[i["outlet"]] = i["visit_count"]
	outlet_id = max(visited_outlet, key=visited_outlet.get) 
	q["preferred_outlet"] = OutletProfile.objects.filter(id=outlet_id)[0].Outletname
	day_diff = (last_order.date()-first_order.date()).days
	if day_diff != 0:
		q["order_pattern"] = str(round(day_diff/q["total_order"],2))+" days"
	else:
		q["order_pattern"] = "First Order"
	if record[0].has_been_here == 0:
		q["customer_type"] = "New"
	else:
		q["customer_type"] = "Loyal"
	return q



class OrderAnalysis(APIView):

	"""
	AddonDetails retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Order analysis as per customer data.

		Data Post: {
		
			"id"                   : "1"
		}

		Response: {

			"success"	: 	True, 
			"message"	: 	"Order analysis as per customer retrieval api worked well",
			"data"		: 	final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Customer Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = CustomerProfile.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided Customer data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["company_id"] = record[0].company_id
				q_dict["name"] = record[0].name
				q_dict["email"] = record[0].email
				q_dict["mobile"] = record[0].mobile
				aa = Order.objects.filter(Company_id=q_dict["company_id"],customer__mobile_number=q_dict["mobile"])
				if aa.count() > 0:
					order_pattern = order_analysis(q_dict)
				else:
					q_dict["order_pattern"] = "N/A"
					order_pattern = q_dict
				final_result.append(order_pattern)
			return Response({
						"success": True, 
						"message": "Order analysis as per customer retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Order analysis as per customer retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})