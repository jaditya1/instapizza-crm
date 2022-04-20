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

#Serializer for api
from rest_framework import serializers
from Product.models import ProductsubCategory, ProductCategory
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

class ProductSubCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductsubCategory
		fields = '__all__'


class SubCategoryCreation(APIView):
	"""
	Sub Category Creation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create product sub category associated with
		category.

		Data Post: {
			"category"		       : "3",
			"subcategory_name"	   : ["Special Pizza","Combo Pizza"]
		}

		Response: {

			"success": True, 
			"message": "Sub-Category creation api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			auth_id = request.user.id
			cid = get_user(auth_id)
			data['Company'] = cid
			err_message = {}
			err_message["category"] =\
				validation_master_anything(data["category"],
					"Category",contact_re, 1)
			if len(data["subcategory_name"]) != 0:
				for i in data["subcategory_name"]:
					err_message["subcategory_name"] = \
						validation_master_anything(i,
						"Sub-Category name",alpha_re, 3)
					if data["category"] != "":
						record_check = ProductsubCategory.objects.filter(Q(subcategory_name__iexact=i),\
													Q(category=data["category"]))
						if record_check.count() != 0:
							err_message["duplicate_subcat"] = \
							"This subcategory already exist under this category!!"
							break
					if err_message["subcategory_name"] != None:
						break
			else:
				err_message["subcategory_name"] = validation_master_anything("t",
						"Sub-Category name",username_re, 3)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			cat_query = ProductCategory.objects.filter(id=data["category"])
			if cat_query.count() != 0:
				pass
			else:
				return Response(
					{
						"success": False,
	 					"message": "Category is not valid!!"
					}
					)
			for i in data["subcategory_name"]:
				create_record = ProductsubCategory.objects.create(category_id=data["category"],\
												subcategory_name=i)
				if create_record:
					pass
				else:
					return Response(
						{
						"success": False,
						"message" : "Sub-Category creation operation is not performed properly!!"
						})
			return Response({
						"success": True, 
						"message": "Sub-Category has been created successfully!!"
						})
		except Exception as e:
			print("Sub-Category creation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


class SubCategoryUpdation(APIView):
	"""
	Sub Category Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to update product sub category associated with
		category.

		Data Post: {
			"id"                   : "1",
			"category"		       : "3",
			"subcategory_name"	   : "Special Pizza"
		}

		Response: {

			"success": True, 
			"message": "Sub-Category Updation api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			from django.db.models import Q
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(str(data["id"]),
					"Sub-Category Id",contact_re, 1)
			err_message["category"] = \
					validation_master_anything(str(data["category"]),
					"Category",contact_re, 1)
			err_message["subcategory_name"] = \
					validation_master_anything(data["subcategory_name"],
					"Sub-Category name",username_re, 3)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			cat_query = ProductCategory.objects.filter(id=data["category"])
			if cat_query.count() != 0:
				pass
			else:
				return Response(
					{
						"success": False,
	 					"message": "Category is not valid!!"
					}
					)
			sucat_query = ProductsubCategory.objects.filter(id=data["id"])
			if sucat_query.count() != 0:
				pass
			else:
				return Response(
					{
						"success": False,
	 					"message": "Sub-Category id is not valid to update!!"
					}
					)
			unique_check = \
			ProductsubCategory.objects.filter(~Q(id=data["id"]),Q(category=data["category"]),\
									Q(subcategory_name__iexact=data['subcategory_name']))
			if unique_check.count()==0:
				serializer = ProductSubCategorySerializer(sucat_query[0],data=data,partial=True)
				if serializer.is_valid():
					data_info = serializer.save()
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(serializer.errors),
						})
			else:
				err_message = {}
				err_message["duplicate_subcat"] = "Sub-Category with this name already exists!!" 
				return Response({
						"success": False, 
						"error" : err_message,
						"message" : "Please correct listed errors!!"
						})
			final_result = []
			final_result.append(serializer.data)
			return Response({
						"success": True, 
						"data" : final_result,
						"message": "Sub-Category has been updated successfully!!"
						})
		except Exception as e:
			print("Sub-Category updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})