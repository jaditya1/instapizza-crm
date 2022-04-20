from rest_framework.views import APIView
from rest_framework.response import Response
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
import os
from django.db.models import Q
from kitchen.models import Ingredient
from ZapioApi.Api.BrandApi.kitchen.serializer import IngredientSerializer
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user


class IngredientCreationUpdation(APIView):

	"""
	Ingredient Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update Ingredient.

		Data Post: {
			"id"                   : "1"(Send this key in update record case,else it is not required!!)
			"name"		           : "dddddd",
			"food_type"                 : "1",
			"image"	               : "dddd.jpg"(type:image)
		}

		Response: {

			"success": True, 
			"message": "Ingredient creation/updation api worked well!!",
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
			Company_id = get_user(auth_id)
			data['company'] = Company_id
			err_message = {}
			if type(data["image"]) != str:
				im_name_path =  data["image"].file.name
				im_size = os.stat(im_name_path).st_size
				if im_size > 500*1024:
					err_message["image_size"] = "Ingredient Image can'nt excced the size more than 10kb!!"
			else:
				data["image"] = None
			err_message["name"] = \
					validation_master_anything(data["name"],
					"Ingredient",alpha_re, 2)

			err_message["food_type"] = \
				validation_master_anything(str(data["food_type"]),
				"Food Type",contact_re, 1)

			if "id" in data:
				unique_check = Ingredient.objects.filter(~Q(id=data["id"]),\
								Q(name__iexact=data["name"]))
			else:
				unique_check = Ingredient.objects.filter(Q(name__iexact=data["name"]))

			if unique_check.count() != 0:
				err_message["unique_check"] = "Ingredient with this name already exists!!"
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
				Ingredient_record = Ingredient.objects.filter(id=data['id'])
				if Ingredient_record.count() == 0:
					return Response(
					{
						"success": False,
	 					"message": "Ingredient data is not valid to update!!"
					}
					)
				else:
					if data["image"] == None:
						data["image"] = Ingredient_record[0].image
					else:
						pass
					data["updated_at"] = datetime.now()
					ingredient_serializer = \
					IngredientSerializer(Ingredient_record[0],data=data,partial=True)
					if ingredient_serializer.is_valid():
						data_info = ingredient_serializer.save()
					else:
						print("something went wrong!!")
						return Response({
							"success": False, 
							"message": str(ingredient_serializer.errors),
							})
			else:
				ingredient_serializer = IngredientSerializer(data=data)
				if ingredient_serializer.is_valid():
					data_info = ingredient_serializer.save()
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(ingredient_serializer.errors),
						})
			final_result = []
			final_result.append(ingredient_serializer.data)
			return Response({
						"success": True, 
						"message": "Ingredient creation/updation api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Ingredient creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})