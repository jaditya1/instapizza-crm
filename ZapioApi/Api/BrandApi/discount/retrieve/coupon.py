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
from discount.models import Coupon
from Customers.models import CustomerProfile


class CouponSerializer(serializers.ModelSerializer):
	class Meta:
		model = Coupon
		fields = '__all__'


class CouponRetrieval1(APIView):
	"""
	Coupon retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Coupon data.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "Coupon retrieval api worked well!!",
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
					"Coupon Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = Coupon.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided Coupon data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["coupon_type"] = []
				coupon_dict = {}
				coupon_dict["label"] = record[0].coupon_type
				coupon_dict["key"] = record[0].coupon_type
				coupon_dict["value"] = record[0].coupon_type
				q_dict["coupon_type"].append(coupon_dict)
				q_dict["coupon_code"] = record[0].coupon_code
				q_dict["frequency"] = record[0].frequency
				q_dict["valid_frm"] = record[0].valid_frm
				q_dict["valid_till"] = record[0].valid_till
				q_dict["category"] = []
				cat_dict = {}
				if record[0].category_id != None:
					cat_dict["label"] = record[0].category.category_name
					cat_dict["key"] = record[0].category_id
					cat_dict["value"] = record[0].category_id
					q_dict["category"].append(cat_dict)
				else:
					pass
				q_dict["product_detail"] = []
				pa = record[0].product_map
				for p in pa:
					query = Product.objects.filter(id=p)
					p_dict = {}
					p_dict["label"] = query[0].product_name
					p_dict["key"] = query[0].id
					p_dict["value"] = query[0].id
					q_dict["product_detail"].append(p_dict)
				q_dict["outlet_detail"] = []
				pa = record[0].outlet_id
				if pa != None:
					for p in pa:
						query = OutletProfile.objects.filter(id=p)
						p_dict = {}
						p_dict["label"] = query[0].Outletname
						p_dict["key"] = query[0].id
						p_dict["value"] = query[0].id
						q_dict["outlet_detail"].append(p_dict)
				else:
					pass
				q_dict["flat_discount"] = record[0].flat_discount
				q_dict["flat_percentage"] = record[0].flat_percentage
				q_dict["is_min_shop"] = record[0].is_min_shop
				q_dict["is_automated"] = record[0].is_automated
				q_dict["min_shoping"] = record[0].min_shoping
				q_dict["max_shoping"] = record[0].max_shoping
				q_dict["active_status"] = record[0].active_status
				final_result.append(q_dict)
			if final_result:
				return Response({
							"success": True, 
							"message": "Coupon retrieval api worked well!!",
							"data": final_result,
							})
			else:
				return Response({
							"success": True, 
							"message": "No Coupon data found!!"
							})
		except Exception as e:
			print("Coupon retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})