import re
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime
from django.db.models import Q

#Serializer for api
from rest_framework import serializers
from Product.models import AddonDetails,Addons



class AssociateAddon(APIView):
	"""
	Associated addons POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide associated addon details within brand.

		Data Post: {
			"id"                   : "94"
		}

		Response: {

			"success": True, 
			"message": "Associated addons details api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			data["id"] = str(data["id"])
			err_message = {}
			err_message["addon"] = \
					validation_master_anything(data["id"],
					"Addon Group Name",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			addon_query = AddonDetails.objects.filter(id=data['id'])
			if addon_query.count() != 0:
				pass
			else:
				return Response(
					{
						"success": False,
	 					"message": "Addon Id is not valid!!"
					}
					)
			final_result = addon_query[0].associated_addons
			final_data = []
			for i in final_result:
				aa = {}
				if 'addon_name' in i:
					name = i['addon_name']
					aa['name'] = name
					aa['price'] = i['price']
					addon_data = Addons.objects.filter(Q(name=name),Q(addon_amount=aa['price']),\
						Q(addon_group_id=data['id']))
					aa['id'] = addon_data[0].id
					final_data.append(aa)
			return Response({
						"success": True, 
						"message": "Associated addons details api worked well!!",
						"data": final_data,
						})
		except Exception as e:
			print("Associated addons Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})

