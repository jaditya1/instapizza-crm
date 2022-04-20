from rest_framework.views import APIView
from rest_framework.response import Response
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
from Product.models import Variant
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

class VariantSerializer(serializers.ModelSerializer):
	class Meta:
		model = Variant
		fields = '__all__'


class VariantCreationUpdation(APIView):
	"""
	Variant Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update product Variant within brand.

		Data Post: {
			"id"                   : "1"(Send this key in update record case,else it is not required!!)
			"variant"		   	   : "Large"
		}

		Response: {

			"success": True, 
			"message": "Variant creation/updation api worked well!!",
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
			user = request.user.id
			cid = get_user(user)
			data['Company'] = cid			
			err_message = {}
			# err_message["variant"] = \
			# 		validation_master_anything(data["variant"],
			# 		"Variant name",username_re, 3)
			err_message['variant'] = \
					only_required(data["variant"], "Variant name")
			unique_check = Variant.objects.filter(variant__iexact=data["variant"],
											Company=cid)
			if unique_check.count() != 0 and "id" not in data:
				err_message["unique_check"] = "Variant with this name already exists!!"
			else:
				pass
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			company_query = Company.objects.filter(id=cid)
			if company_query.count() != 0:
				data["Company"] = cid
			else:
				return Response(
					{
						"success": False,
	 					"message": "Company is not valid!!"
					}
					)
			if "id" in data:
				variant_record = Variant.objects.filter(id=data['id'])
				if variant_record.count() == 0:
					return Response(
					{
						"success": False,
	 					"message": "Category data is not valid to update!!"
					}
					)
				else:
					unique_check = \
					Variant.objects.filter(~Q(id=data["id"]),\
									Q(variant__iexact=data['variant']),\
									Q(Company=cid))
					if unique_check.count() == 0:
						data["updated_at"] = datetime.now()
						variant_serializer = \
						VariantSerializer(variant_record[0],data=data,partial=True)
						if variant_serializer.is_valid():
							data_info = variant_serializer.save()
							info_msg = "Vriant updated successfully!!"
						else:
							print("something went wrong!!")
							return Response({
								"success": False, 
								"message": str(variant_serializer.errors),
								})
					else:
						err_message = {}
						err_message["unique_check"] = "Variant with this name already exists!!"
						return Response({
									"success": False,
									"error" : err_message,
									"message" : "Please correct listed errors!!"
									})
			else:
				variant_serializer = VariantSerializer(data=data)
				if variant_serializer.is_valid():
					data_info = variant_serializer.save()
					info_msg = "Vriant created successfully!!"
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(variant_serializer.errors),
						})
			final_result = []
			final_result.append(variant_serializer.data)
			return Response({
						"success": True, 
						"message": info_msg,
						"data": final_result,
						})
		except Exception as e:
			print("Variant creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})