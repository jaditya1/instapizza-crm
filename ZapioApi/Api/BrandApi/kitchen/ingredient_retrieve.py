from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
from zapio.settings import Media_Path

#Serializer for api
from rest_framework import serializers
from kitchen.models import Ingredient


class IngredientRetrieval(APIView):

	"""
	Ingredient POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Ingredient data.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "Ingredient retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"FoodType Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = Ingredient.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided Ingredient data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["name"] = record[0].name
				q_dict["foodtype_detail"] = []
				food_dict = {}
				food_dict["label"] = record[0].food_type.food_type
				food_dict["key"] = record[0].food_type_id
				food_dict["value"] = record[0].food_type_id
				q_dict["foodtype_detail"].append(food_dict)
				full_path = Media_Path
				q_dict["image"] = record[0].image
				if q_dict["image"] != None and q_dict["image"]!="":
					q_dict["image"] = full_path+str(q_dict["image"])
				else:
					q_dict["image"] = None
				q_dict["active_status"] = record[0].active_status
				q_dict["created_at"] = record[0].created_at
				q_dict["updated_at"] = record[0].updated_at
				final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "Ingredient retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("FoodType retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})