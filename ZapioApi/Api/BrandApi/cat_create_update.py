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
from django.db.models import Q
import os
from django.db.models import Max
from ZapioApi.Api.BrandApi.Validation.category_error_check import *
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

#Serializer for api
from rest_framework import serializers
from Product.models import ProductCategory

class ProductCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductCategory
		fields = '__all__'


class CategoryCreationUpdation(APIView):
	"""
	Category Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update product category within brand.

		Data Post: {
			"id"                   : "1"(Send this key in update record case,else it is not required!!)
			"category_name"		   : "Pizza",
			"category_code"		   : "123456",
			"company_auth_id" 	   : "3",
			"priority"             : "1"
		}

		Response: {

			"success": True, 
			"message": "Category creation/updation api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			auth_id = request.user.id
			data["category_code"] = data["category_code"].strip()
			validation_check = err_check(data)
			cid = get_user(auth_id)
			data['Company'] = cid
			if validation_check != None:
				return Response(validation_check) 
			unique_check = unique_record_check(data,cid)
			if unique_check != None:
				return Response(unique_check)

			if "id" in data:
				category_record = ProductCategory.objects.filter(id=data['id'])
				if category_record.count() == 0:
					return Response(
					{
						"success": False,
	 					"message": "Category data is not valid to update!!"
					}
					)
				else:
					data["updated_at"] = datetime.now()
					category_serializer = \
					ProductCategorySerializer(category_record[0],data=data,partial=True)
					if category_serializer.is_valid():
						data_info = category_serializer.save()
					else:
						print("something went wrong!!")
						return Response({
							"success": False, 
							"message": str(category_serializer.errors),
							})
			else:
				category_serializer = ProductCategorySerializer(data=data)
				if category_serializer.is_valid():
					data_info = category_serializer.save()
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(category_serializer.errors),
						})
			final_result = []
			final_result.append(category_serializer.data)
			return Response({
						"success": True, 
						"message": "Category creation/updation api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Category creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})

