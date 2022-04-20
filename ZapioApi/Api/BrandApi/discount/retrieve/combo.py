from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
#Serializer for api
from rest_framework import serializers
from Product.models import Product, AddonDetails
from discount.models import QuantityCombo, PercentCombo

class QuantityComboRetrieval(APIView):
	"""
	Quantity Combo retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Quantity Combo data.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "Quantity Combo retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Combo Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = QuantityCombo.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided Quantity Combo data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["combo_name"] = record[0].combo_name
				q_dict["product_detail"] = []
				p_dict = {}
				p_dict["label"] = record[0].product.product_name
				p_dict["key"] = record[0].product_id
				p_dict["value"] = record[0].product_id
				q_dict["product_detail"].append(p_dict)
				q_dict["free_product_detail"] = []
				f_p_dict = {}
				f_p_dict["label"] = record[0].free_product.product_name
				f_p_dict["key"] = record[0].free_product_id
				f_p_dict["value"] = record[0].free_product_id
				q_dict["free_product_detail"].append(f_p_dict)
				q_dict["product_quantity"] = record[0].product_quantity
				q_dict["free_pro_quantity"] = record[0].free_pro_quantity
				q_dict["valid_frm"] = record[0].valid_frm
				q_dict["valid_till"] = record[0].valid_till
				q_dict["active_status"] = record[0].active_status
				final_result.append(q_dict)
			if final_result:
				return Response({
							"success": True, 
							"message": "Quantity Combo retrieval api worked well!!",
							"data": final_result,
							})
			else:
				return Response({
							"success": True, 
							"message": "No Quantity Combo data found!!"
							})
		except Exception as e:
			print("Quantity Combo retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


class PercentComboRetrieval(APIView):
	"""
	Percent Combo retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Percent Combo data.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "Percent Combo retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Combo Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = PercentCombo.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided Percent Combo data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["pcombo_name"] = record[0].pcombo_name
				q_dict["product_detail"] = []
				p_dict = {}
				p_dict["label"] = record[0].product.product_name
				p_dict["key"] = record[0].product_id
				p_dict["value"] = record[0].product_id
				q_dict["product_detail"].append(p_dict)
				q_dict["discount_product_detail"] = []
				d_p_dict = {}
				d_p_dict["label"] = record[0].discount_product.product_name
				d_p_dict["key"] = record[0].discount_product_id
				d_p_dict["value"] = record[0].discount_product_id
				q_dict["discount_product_detail"].append(d_p_dict)
				q_dict["discount_percent"] = record[0].discount_percent
				q_dict["valid_frm"] = record[0].valid_frm
				q_dict["valid_till"] = record[0].valid_till
				q_dict["active_status"] = record[0].active_status
				final_result.append(q_dict)
			if final_result:
				return Response({
							"success": True, 
							"message": "Percent Combo retrieval api worked well!!",
							"data": final_result,
							})
			else:
				return Response({
							"success": True, 
							"message": "No Percent Combo data found!!"
							})
		except Exception as e:
			print("Percent Combo retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})