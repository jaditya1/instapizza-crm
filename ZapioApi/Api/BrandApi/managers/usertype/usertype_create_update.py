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
from ZapioApi.Api.BrandApi.managers.Validation.usertype_error_check import *

#Serializer for api
from rest_framework import serializers
from UserRole.models import UserType
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user


class UserTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserType
		fields = '__all__'


class UserTypeCreationUpdation(APIView):
	"""
	UserType Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update User Types.

		Data Post: {
			"id"                   : "1",(Send this key in update record case,else it is not required!!)
			"user_type"		   	   : "Outlet manager"
		}

		Response: {

			"success": True, 
			"message": "UserType creation/updation api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			from Brands.models import Company
			data = request.data
			auth_id = request.user.id
			Company_id = get_user(auth_id)
			validation_check = err_check(data)
			if validation_check != None:
				return Response(validation_check) 
			integrity_check = record_integrity_check(data,auth_id)
			if integrity_check != None:
				return Response(integrity_check)
			data["Company"] = Company_id
			if "id" in data:
				record = UserType.objects.filter(id=data['id'])
				if record.count() == 0:
					return Response(
					{
						"success": False,
	 					"message": "User Type data is not valid to update!!"
					}
					)
				else:
					data["updated_at"] = datetime.now()
					serializer = \
					UserTypeSerializer(record[0],data=data,partial=True)
					if serializer.is_valid():
						data_info = serializer.save()
						info_msg = "User Type is updated successfully!!"
					else:
						print("something went wrong!!")
						return Response({
							"success": False, 
							"message": str(addon_serializer.errors),
							})
			else:
				serializer = UserTypeSerializer(data=data)
				if serializer.is_valid():
					data_info = serializer.save()
					info_msg = "User Type is created successfully!!"
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(addon_serializer.errors),
						})
			return Response({
						"success": True, 
						"message": info_msg
						})
		except Exception as e:
			print("UserType creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})