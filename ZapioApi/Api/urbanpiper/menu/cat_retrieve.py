from rest_framework.views import APIView
from rest_framework.response import Response
import re
from urbanpiper.models import CatOutletWise
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from rest_framework_tracking.mixins import LoggingMixin

class CatRetrieval(LoggingMixin,APIView):
	"""
	Category retrieval Outletwise POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Outletwise category data.

		Data Post: {
			"id"                   : 	"3"
		}

		Response: {

			"success"	: 	True, 
			"message"	: 	"API worked well!!",
			"data"		:	final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			data["id"] = str(data["id"])
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Category Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = CatOutletWise.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "DATA IS NOT FOUND!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["category_name"] = record[0].sync_cat.category.category_name
				q_dict["outlet"] = record[0].sync_outlet.outlet.Outletname
				q_dict["priority"] = record[0].priority
				final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "API worked well!!",
						"data": final_result,
						})
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
