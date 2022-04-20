from rest_framework.views import APIView
from rest_framework.response import Response
from UserRole.models import UserType, MainRoutingModule, RoutingModule, SubRoutingModule
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from ZapioApi.Api.BrandApi.managers.Validation.route_error_check import *

class RouteListing(APIView):
	"""
	Route listing POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Routes.

		Data Post: {

			"main_routes" 	    : [1,2]
		}

		Response: {

			"success": true,
		    "data": final_result,
		    "message": "Route fetching successful!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			validation_check = err_check(data)
			if validation_check != None:
				return Response(validation_check) 
			integrity_check = record_integrity_check(data)
			
			if integrity_check != None:
				return Response(integrity_check)
			record = RoutingModule.objects.filter(active_status=1)
			main_routes = data["main_routes"]
			final_result = []
			for i in main_routes:
				q = RoutingModule.objects.filter(active_status=1,main_route=i)
				if q.count() != 0:
					for j in q:
						record_dict = {}
						record_dict['module_id'] = j.id
						record_dict['module_name'] = j.module_name
						final_result.append(record_dict)
				else:
					pass
			return Response({
					"success": True, 
					"data": final_result})
		except Exception as e:
			print("Route listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})