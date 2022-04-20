from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.Api.BrandApi.managers.Validation.manager_error_check import *

#Serializer for api
from rest_framework import serializers
from UserRole.models import ManagerProfile
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from rest_framework_tracking.mixins import LoggingMixin


class ManagerSerializer(serializers.ModelSerializer):
	class Meta:
		model = ManagerProfile
		fields = '__all__'

class ManagerCreationUpdation(LoggingMixin,APIView):
	"""
	Manager Creation/Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create new outlets within brand.

		Data Post: {
			
			"id"                    : "1"(In case of updation, optional key)
			"username"			    : "insta_assist_mgr",
			"password"		        : "123456",
			"user_type" 			: "1",
			"manager_name"          : "Ujjwal",
			"email"					: "test@gmail.com",
			"mobile"				: "9999999999",
		}

		Response: {

			"success": True,
			"message": "Manager is registered successfully under your brand!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			auth_id = request.user.id
			Company_id = get_user(auth_id)
			data["Company"] = Company_id
			data["auth_username"] = str(data["Company"])+"m"+str(data["username"])
			validation_check = err_check(data)
			if validation_check != None:
				return Response(validation_check)
			integrity_check = record_integrity_check(data,auth_id)
			if integrity_check != None:
				return Response(integrity_check)
			if "id" not in data:
				create_user = User.objects.create_user(
							username=data["auth_username"],
							password=data['password'],
							is_staff=False,
							is_active=True
							)
				if create_user:
					data["active_status"] = 1
					data["auth_user"] = create_user.id
					serializer = ManagerSerializer(data=data)
					if serializer.is_valid():
						data_info = serializer.save()
						info_msg = "Manager is registered successfully under your brand!!"
					else:
						print(str(serializer.errors))
						return Response({
							"success": False, 
							"message": str(serializer.errors)
							})
				else:
					return Response(
					{
					"success": False,
					"message": "Some error occured in the process of manager profile creation!!"
					}
					)
			else:
				del data["username"]
				record = ManagerProfile.objects.filter(id=data["id"])
				manager_auth_id = record[0].auth_user_id
				check_the_user = User.objects.filter(id=manager_auth_id).first()
				check_the_user.set_password(data["password"])
				check_the_user.save()
				data["updated_at"] = datetime.now()
				serializer = ManagerSerializer(record[0],data=data,partial=True)
				if serializer.is_valid():
					data_info = serializer.save()
					info_msg = "Manager record is updated successfully!!"
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
			print("Manager Creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})