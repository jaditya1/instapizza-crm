from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
import os
from django.db.models import Max
from ZapioApi.Api.BrandApi.listing.listing import  ProductlistingSerializer

#Serializer for api
from rest_framework import serializers
from Product.models import FeatureProduct, Product, ProductCategory, ProductsubCategory,\
	AddonDetails
from Brands.models import Company
from ZapioApi.Api.BrandApi.Validation.feature_error_check import *
from rest_framework import serializers
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

class FeatureSerializer(serializers.ModelSerializer):
	class Meta:
		model = FeatureProduct
		fields = '__all__'

class Feature(APIView):
	"""
	Feature Product Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update fetaured products within brand.

		Data Post: {

			"id"                   : "1"(Send this key in update record case,else it is not required!!)
			"feature_product"      : [1, 2],
			"outlet"               : 1
		}
		Response: {

			"success": True, 
			"message": "Feature Product creation/updation api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			from django.db.models import Q
			data = request.data
			user = request.user.id
			cid = get_user(user)
			data['company'] = cid
			data['company_auth_id'] = request.user.id
			validation_check = err_check(data)
			if validation_check != None:
				return Response(validation_check) 
			record_check = record_integrity_check(data)
			if record_check != None:
				return Response(record_check)
			if "id" in data:
				record = FeatureProduct.objects.filter(id=data['id'])
				if record.count() == 0:
					return Response(
					{
						"success": False,
						"message": "Feature Product data is not valid to update!!"
					}
					)
				else:
					data["updated_at"] = datetime.now()
					serializer = \
					FeatureSerializer(record[0],data=data,partial=True)
					if serializer.is_valid():
						data_info = serializer.save()
						info_msg = "Featured product is updated successfully!!"
					else:
						print("something went wrong!!")
						return Response({
							"success": False, 
							"message": str(serializer.errors),
							})
			else:
				data["active_status"] = 1
				serializer = FeatureSerializer(data=data)
				if serializer.is_valid():
					data_info = serializer.save()
					info_msg = "Featured product is created successfully!!"
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(serializer.errors),
						})
			return Response({
						"success": True, 
						"message": info_msg,
						})
		except Exception as e:
			print("Feature Product creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})