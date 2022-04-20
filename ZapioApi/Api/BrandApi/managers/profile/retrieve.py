from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *

#Serializer for api
from rest_framework import serializers
from UserRole.models import ManagerProfile
from Outlet.models import DeliveryBoy,OutletProfile


class ManagerRetrieval(APIView):
	"""
	Manager retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Manager data.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "Manager retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Manager Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = ManagerProfile.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided manager data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["user_type_details"] = []
				user_type_dict = {}
				user_type_dict["label"] = record[0].user_type.user_type
				user_type_dict["key"] = record[0].user_type_id
				user_type_dict["value"] = record[0].user_type_id
				q_dict["user_type_details"].append(user_type_dict)
				q_dict["active_status"] = record[0].active_status
				q_dict["username"] = record[0].username
				q_dict["manager_name"] = record[0].manager_name
				q_dict["password"] = record[0].password
				q_dict["email"] = record[0].email
				q_dict["mobile"] = record[0].mobile


				q_dict['outlet'] = []
				if len(record[0].outlet) > 0:
					a = record[0].outlet
					for i in a:
						out = {}
						out['label'] = OutletProfile.objects.filter(id=str(i))[0].Outletname
						out['key'] = str(i)
						out['value'] = str(i)
						q_dict['outlet'].append(out)
				else:
					pass
				final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "Manager retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Manager retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})