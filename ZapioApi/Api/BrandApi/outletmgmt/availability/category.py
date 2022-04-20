from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from Product.models import Product, Product_availability, Category_availability, ProductCategory
from ZapioApi.api_packages import *
from Outlet.models import OutletProfile
import re
from ZapioApi.Api.BrandApi.outletmgmt.availability.available import *
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from _thread import start_new_thread
from PosApi.Api.outletmgmt.outletwiselisting.available import MenuSync



class BrandLevelCategory(APIView):
	"""
	Category availability Post API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to make Category available or unavailable within outlet.

		Data Post: {
			"is_available"  : "false",
			"id"            : "1",
			"outlet"        : "21"
		}

		Response: {

			"success": True, 
			"message": "Category is unavailable now!!",

		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			auth_id = request.user.id
			Company_id = get_user(auth_id)
			cat_check = CategoryAvailable(data,Company_id)
			if cat_check !=None:
				return Response(cat_check) 
			else:
				if data['is_available'] ==False:
					msg = "Category is already unavailable!!"
				else:
					msg = "Category is already available!!"
				return Response({
					"success" : False,
					"message" : msg
					})
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})