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
from Product.models import Product, AddonDetails,ProductCategory
from discount.models import Coupon,Discount
from Customers.models import CustomerProfile
from UserRole.models import UserType

class CouponSerializer(serializers.ModelSerializer):
	class Meta:
		model = Discount
		fields = '__all__'


class CouponRetrieval(APIView):
	"""
	Coupon retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Discount data.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "Discount retrieval api worked well!!",
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
					"Discount Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = Discount.objects.filter(id=data['id'])
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
				q_dict["discount_type"] = []
				coupon_dict = {}
				coupon_dict["label"] = record[0].discount_type
				coupon_dict["key"] = record[0].discount_type
				coupon_dict["value"] = record[0].discount_type
				q_dict["discount_type"].append(coupon_dict)
				q_dict["valid_frm"] = record[0].valid_frm
				q_dict["discount_name"] = record[0].discount_name
				q_dict["valid_till"] = record[0].valid_till
				q_dict["is_all_category"] = record[0].is_all_category
				q_dict["is_all_product"] = record[0].is_all_product
				q_dict["category"] = []				
				pa = record[0].category_map
				if pa != None:
					for p in pa:
						query = ProductCategory.objects.filter(id=p)
						p_dict = {}
						p_dict["label"] = query[0].category_name
						p_dict["key"] = query[0].id
						p_dict["value"] = query[0].id
						q_dict["category"].append(p_dict)
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
				q_dict["user_roll"] = []
				pa = record[0].user_roll
				for p in pa:
					query = UserType.objects.filter(id=p)
					p_dict = {}
					p_dict["label"] = query[0].user_type
					p_dict["key"] = query[0].id
					p_dict["value"] = query[0].id
					q_dict["user_roll"].append(p_dict)


				q_dict["outlet_detail"] = []
				pa = record[0].outlet_id
				for p in pa:
					query = OutletProfile.objects.filter(id=p)
					p_dict = {}
					p_dict["label"] = query[0].Outletname
					p_dict["key"] = query[0].id
					p_dict["value"] = query[0].id
					q_dict["outlet_detail"].append(p_dict)

				q_dict["flat_discount"] = record[0].flat_discount
				q_dict["flat_percentage"] = record[0].flat_percentage
				q_dict["is_min_shop"] = record[0].is_min_shop
				q_dict["is_reason_required"] = record[0].is_reason_required
				q_dict["min_shoping"] = record[0].min_shoping
				q_dict["max_shoping"] = record[0].max_shoping
				q_dict["active_status"] = record[0].active_status
				final_result.append(q_dict)
			if final_result:
				return Response({
							"success": True, 
							"message": "Discount retrieval api worked well!!",
							"data": final_result,
							})
			else:
				return Response({
							"success": True, 
							"message": "No Discount data found!!"
							})
		except Exception as e:
			print("Discount retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})