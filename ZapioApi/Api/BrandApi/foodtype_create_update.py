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
from django.db.models import Q
from ZapioApi.Api.BrandApi.listing.listing import FoodTypelistingSerializer
from Product.models import FoodType
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user


class FoodTypeCreationUpdation(APIView):
	"""
	FoodType Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update Food Type.

		Data Post: {
			"id"                   : "1"(Send this key in update record case,else it is not required!!)
			"food_type"		       : "Veg",
			"foodtype_image"	   : "veg.jpg"(type:image)
		}

		Response: {

			"success": True, 
			"message": "Food Type creation/updation api worked well!!",
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
			err_message = {}
			if type(data["foodtype_image"]) != str:
				im_name_path =  data["foodtype_image"].file.name
				im_size = os.stat(im_name_path).st_size
				if im_size > 10*1024:
					err_message["image_size"] = "Food type logo can'nt excced the size more than 10kb!!"
			else:
				data["foodtype_image"] = None
			err_message["food_type"] = \
					validation_master_anything(data["food_type"],
					"Food type",alpha_re, 2)
			if "id" in data:
				unique_check = FoodType.objects.filter(~Q(id=data["id"]),\
								Q(food_type__iexact=data["food_type"]))
			else:
				unique_check = FoodType.objects.filter(Q(food_type__iexact=data["food_type"]))
			if unique_check.count() != 0:
				err_message["unique_check"] = "Food type with this name already exists!!"
			else:
				pass
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			data["active_status"] = 1
			if "id" in data:
				FoodType_record = FoodType.objects.filter(id=data['id'])
				if FoodType_record.count() == 0:
					return Response(
					{
						"success": False,
	 					"message": "Food Type data is not valid to update!!"
					}
					)
				else:
					if data["foodtype_image"] == None:
						data["foodtype_image"] = FoodType_record[0].foodtype_image
					else:
						pass
					data["updated_at"] = datetime.now()
					FoodType_serializer = \
					FoodTypelistingSerializer(FoodType_record[0],data=data,partial=True)
					if FoodType_serializer.is_valid():
						data_info = FoodType_serializer.save()
					else:
						print("something went wrong!!")
						return Response({
							"success": False, 
							"message": str(FoodType_serializer.errors),
							})
			else:
				FoodType_serializer = FoodTypelistingSerializer(data=data)
				if FoodType_serializer.is_valid():
					data_info = FoodType_serializer.save()
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(FoodType_serializer.errors),
						})
			final_result = []
			final_result.append(FoodType_serializer.data)
			return Response({
						"success": True, 
						"message": "Food Type creation/updation api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Food Type creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})