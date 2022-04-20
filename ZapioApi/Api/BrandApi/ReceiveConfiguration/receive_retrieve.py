from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime

#Serializer for api
from rest_framework import serializers
from Product.models import Tag,Product
from Configuration.models import HeaderFooter



class ReceiveRetrieve(APIView):

	"""
	Receipt Configuration POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for retrieval of Receipt Configuration data.

		Data Post: {
			"id"                   : "1"
		}

		Response: {
			"success": True, 
			"message": "Receipt Configuration retrieval api worked well!!",
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
					"Receipt Configuration Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = HeaderFooter.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Receipt Configuration is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["header"] = record[0].header_text
				q_dict["footer"] = record[0].footer_text
				q_dict["gst"] = record[0].gst
				q_dict["outlet_detail"] = []
				out_dict = {}
				out_dict["label"] = record[0].outlet.Outletname
				out_dict["key"] = record[0].outlet_id
				out_dict["value"] = record[0].outlet_id
				q_dict["outlet_detail"].append(out_dict)
				q_dict["outlet"] = record[0].outlet_id
				q_dict["active_status"] = record[0].active_status
				q_dict["created_at"] = record[0].created_at
				q_dict["updated_at"] = record[0].updated_at
				final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "Receipt Configuration retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Receipt Configuration retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})