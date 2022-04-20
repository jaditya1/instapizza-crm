from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
from Orders.models import Order
from Brands.models import Company
import dateutil.parser
from urbanpiper.models import ProductSync
from Product.models import Variant
from ZapioApi.Api.download_token import token_create, token_delete 

def result_data(order_record):
	order_result = []
	product_ids = []
	is_id_found = 1
	for i in order_record:
		order_desc = i.order_description
		if i.is_aggregator == True:
			for j in order_desc:
				data_dict = {}
				data_dict["is_aggregator"] = True
				final_product_id = j["final_product_id"]
				variant = "N/A"
				product_record = \
				ProductSync.objects.filter(id=j["final_product_id"])
				if product_record.count() == 1:
					product_name = \
					product_record[0].product.product_name
					if product_record[0].variant != None:
						variant = product_record[0].variant.variant
					else:
						pass
				else:
					pass
				data_dict["final_product_id"] = final_product_id
				data_dict["product_name"] = product_name
				data_dict["variant"] = variant
				if i.rating == None:
					data_dict["rating"] = "N/A"
				else:
					data_dict["rating"] = i.rating
				order_result.append(data_dict)
		else:
			for j in order_desc:
				order_dict = {}
				order_dict["is_aggregator"] = False
				order_dict["variant"] = "N/A"
				final_product_record = \
					ProductSync.objects.filter(product=j["id"])
				if "size" in j:
					if j["size"] != "" and j["size"] != "N/A":
						v_record = Variant.objects.filter(variant__iexact=j["size"])
						if v_record.count() != 0:
							v_id = v_record[0].id
						else:
							v_id = "N/A"
					else:
						v_id = "N/A"
				else:
					v_id = "N/A"
				if v_id == "N/A":
					pass
				else:
					final_product_record = final_product_record.filter(variant=v_id)
				if final_product_record.count() != 0:
					final_product_id = final_product_record[0].id
					order_dict["final_product_id"] = str(final_product_id)
					order_dict["product_name"] = j["name"]
					# order_dict["variant"] = final_product_record[0].variant.variant
				else:
					is_id_found = 0
				if is_id_found == 1:
					if final_product_record[0].variant != None:
						order_dict["variant"] = final_product_record[0].variant.variant
					else:
						pass
				else:
					pass

				if is_id_found == 1:
					order_dict["final_product_id"] = final_product_id
					order_dict["product_name"] = order_dict["product_name"]
					order_dict["variant"] = order_dict["variant"]
					if i.rating == None:
						order_dict["rating"] = "N/A"
					else:
						order_dict["rating"] = i.rating
					order_result.append(order_dict)
					
				else:
					pass
		
	result = []
	product_ids = []
	for i in order_result:
		if i["final_product_id"] not in product_ids:
			product_ids.append(i["final_product_id"])
		else:
			pass

	total_count = 0
	for i in product_ids:
		data_dict = {}

		data_dict["order_count"] = 0
		data_dict["total_rating"] = 0
		data_dict["rated_order"] = 0
		is_rated = 0
		for j in order_result:
			if j["rating"] == "N/A":
				rating = 0
				is_rated = 0
			else:
				rating = j["rating"]
				is_rated = 1
			if i == j["final_product_id"]:
				data_dict["order_count"] = data_dict["order_count"]+1
				data_dict["total_rating"] = data_dict["total_rating"]+rating
				data_dict["product_name"] = j["product_name"]
				data_dict["variant"] = j["variant"]
				data_dict["final_product_id"] = i
				if is_rated == 1:
					data_dict["rated_order"] = data_dict["rated_order"]+1
				else:
					pass
			else:
				pass
		# for i in order_record:
		# 	data_dict["outlet_name"] = i.outlet.Outletname
		total_count = total_count + data_dict["order_count"]
		result.append(data_dict)


	for i in result:
		if i["rated_order"] == 0:
			i["avg_rating"] = "N/A"
		else:
			i["avg_rating"] = round((i["total_rating"]/i["rated_order"]),2)
	return result

class ProductLevelReport(APIView):
	"""
	Product Level Report listing POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing all product report based on provided
		date range.

		Data Post:{

			"is_all"		: 	""(True or False)
			"start_date"	: 	"2020-08-15",
			"end_date"		: 	"2020-08-17",
			"outlet_ids"	: 	"18",

		}


		Response: {

			"success"	: 	True, 
			"message"	: 	"Active product data retrieval api worked well!!",
			"data"		: 	final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			err_message = {}
			s_date = data['start_date']
			e_date = data['end_date']
			is_all = data['is_all']
			if is_all != True and is_all != False:
				err_message['is_all'] = "Flag is not set properly!!"
			else:
				pass
			try:
				start_date = dateutil.parser.parse(s_date)
				end_date = dateutil.parser.parse(e_date)
				if start_date < end_date:
					pass
				else:
					err_message["date"] = "Please provide meaning full date range!!"
			except Exception as e:
				err_message["date"] = "Please provide meaning full date range!!"
			if is_all == False:
				try:
					data["outlet_ids"] = int(data["outlet_ids"])
				except Exception as e:
					err_message["outlet"] = "Outlet is not valid!!"
			else:
				pass
			if any(err_message.values())==True:
					return Response({
						"success"	: 	False,
						"error" 	: 	err_message,
						"message" 	: 	"Please correct listed errors!!"

						})
			generate_token = token_create()
			token_id = generate_token["token_id"]
			download_token = generate_token["download_token"]
			if is_all == False:
				order_record = Order.objects.filter(order_time__date__gte=start_date,\
													order_time__date__lte=end_date, \
													outlet=data["outlet_ids"])
			else:
				order_record = Order.objects.filter(order_time__date__gte=start_date, \
													order_time__date__lte=end_date)

			result = result_data(order_record)

			return Response({
				"success"			:	True,
				"data"				:	result,
				"token_id"			:	token_id,
				"download_token"	:	download_token
				})
		except Exception as e:
			return Response({
				"success"	: 	False, 
				"message"	: 	"Error happened!!", 
				"errors"	: 	str(e)
				})