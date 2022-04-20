from rest_framework.views import APIView
from rest_framework.response import Response
import re
from urbanpiper.models import CatOutletWise
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from rest_framework_tracking.mixins import LoggingMixin


class SetPriority(LoggingMixin,APIView):
	"""
	Outletwise Catregory Priority SEt POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to set priority of category outletwise.

		Data Post: {
			"id"                   : "1",
			"priority"		       : "3",
		}

		Response: {

			"success"	: 	True, 
			"message"	: 	"Priority is updated!!",
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			from django.db.models import Q
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(str(data["id"]),
					"Category Id",contact_re, 1)
			err_message["priority"] = \
					validation_master_anything(str(data["priority"]),
					"Priority",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			data["priority"] = int(data["priority"])
			query = CatOutletWise.objects.filter(id=data["id"])
			if query.count() != 0:
				outlet = query[0].sync_outlet_id
				record_check =  CatOutletWise.objects.filter(~Q(id=data["id"]), Q(sync_outlet=outlet),\
											Q(priority=data["priority"]))
				if record_check.count() == 0:
					record_update = query.update(priority=data["priority"])
				else:
					err_message = {}
					err_message["priority"] = "This priority is already assigned to some other category!!"
					return Response({
						"success"	: 	False,
						"error" 	: 	err_message,
						"message" 	: 	"Please correct listed errors!!"
					})
			else:
				return Response(
					{
						"success": False,
	 					"message": "Category is not valid!!"
					}
					)
			return Response({
						"success": True, 
						"message": "Priority is updated!!"
						})
		except Exception as e:

			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})