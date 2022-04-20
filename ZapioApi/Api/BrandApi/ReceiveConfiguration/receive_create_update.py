from rest_framework.views import APIView
from rest_framework.response import Response
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
import os
from django.db.models import Q
from Product.models import Tag
from ZapioApi.Api.BrandApi.tag.serializer import TagSerializer
from Brands.models import Company
from Outlet.models import *
from UserRole.models import ManagerProfile
from Configuration.models import HeaderFooter
class ReceiveCreationUpdation(APIView):

	"""
	Receipt Configuration Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update Receipt Configuration.

		Data Post: {
			"id"                       : "1"(Send this key in update record case,else it is not required!!)
			"outlet"				   : "1"
			"header"                   : "demo text"
			"footer"				   : "Demo text"
			"gst"					   : "3433543543efefe"
		}

		Response: {

			"success": True, 
			"message": "Receipt Configuration creation/updation api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			err_message = {}
			data = request.data
			user = request.user.id
			is_outlet = OutletProfile.objects.filter(auth_user_id=user)
			is_brand = Company.objects.filter(auth_user_id=user)
			is_cashier = ManagerProfile.objects.filter(auth_user_id=user)
			if is_cashier.count() > 0:
				cid = ManagerProfile.objects.filter(auth_user_id=user)[0].Company_id
			else:
				pass
			if is_outlet.count() > 0:
				outlet = OutletProfile.objects.filter(auth_user_id=user)
				cid = outlet[0].Company_id
			else:
				pass
			if is_brand.count() > 0:
				outlet = Company.objects.filter(auth_user_id=user)
				cid = outlet[0].id
			else:
				pass
			data['Company'] = cid
			err_message["outler"] = only_required(data["outlet"],"Outlet")
			err_message["header"] = only_required(data["header"],"Header Text")
			err_message["footer"] = only_required(data["footer"],"Footer Text")
			err_message["gst"] = only_required(data["gst"],"Gst")
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			if "id" in data:
				unique_check = HeaderFooter.objects.filter(~Q(id=data["id"]),\
								Q(outlet_id=data["outlet"]))
				if unique_check.count() > 0:
					err_message["unique_check"] = "Outlet already exists!!"
					return Response({
							"success": False,
							"error" : err_message,
							"message" : "Please correct listed errors!!"
					})
			else:
				unique_check = HeaderFooter.objects.filter(Q(outlet_id=data["outlet"]))
				if unique_check.count() > 0:
					err_message["unique_check"] = "Outlet already exists!!"
					return Response({
							"success": False,
							"error" : err_message,
							"message" : "Please correct listed errors!!"
					})
			data["active_status"] = 1
			if "id" in data:
				header_record = HeaderFooter.objects.filter(id=data['id'])
				if header_record.count() == 0:
					return Response(
					{
						"success": False,
						"message": "HeaderFooter data is not valid to update!!"
					}
					)
				else:
					data["updated_at"] = datetime.now()
					update_data = \
					header_record.update(outlet_id=data['outlet'],\
					header_text=data["header"],footer_text=data["footer"],\
					gst=data["gst"],company_id=data['Company'],
					updated_at=datetime.now())
					if update_data:
						info_msg = "Receipt Configuration is updated successfully!!"
					else:
						print("something went wrong!!")
						return Response({
							"success": False, 
							"message": str(serializer.errors),
							})
			else:
				p_query = \
					HeaderFooter.objects.create(outlet_id=data['outlet'],
					header_text=data["header"],footer_text=data["footer"],\
					gst=data["gst"],company_id=data['Company'])
				if p_query:
					data_info=p_query
					info_msg = "Receipt Configuration is created successfully!!"
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(serializer.errors),
						})
			return Response({
						"success": True, 
						"message": info_msg
						})
		except Exception as e:
				print(str(e))
				return Response({"success": False, 
								"message": "Error happened!!", 
								"errors": str(e)})
