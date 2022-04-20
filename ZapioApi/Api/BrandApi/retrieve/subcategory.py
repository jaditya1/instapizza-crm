from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, \
	HTTP_406_NOT_ACCEPTABLE, HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime

#Serializer for api
from rest_framework import serializers
from Product.models import ProductCategory,ProductsubCategory

class ProductsubCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductsubCategory
		fields = '__all__'


class SubCategoryRetrieval(APIView):
	"""
	Sub-Category retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of subcategory data within brand.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "Sub-Category retrieval api worked well!!",
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
					"Category Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = ProductsubCategory.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Required Sub-Category data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["cat_id"] = record[0].category_id
				q_dict["category_name"] = record[0].category.category_name
				q_dict["subcategory_name"] = record[0].subcategory_name
				q_dict["active_status"] = record[0].active_status
				q_dict["created_at"] = record[0].created_at
				q_dict["updated_at"] = record[0].updated_at
				final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "Sub-Category retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Sub-Category retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
