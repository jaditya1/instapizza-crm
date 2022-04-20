from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from Product.models import Product, Product_availability, Category_availability, ProductCategory
from ZapioApi.api_packages import *
import re
from ZapioApi.Api.BrandApi.outletmgmt.availability.available import *
from rest_framework_tracking.mixins import LoggingMixin
from urbanpiper.models import ProductSync
from Outlet.models import OutletProfile
from Product.models import AddonDetails, Addons
from ZapioApi.Api.urbanpiper.sync.item_action import OptionAction


class PosLevelAddonavail(LoggingMixin,APIView):
	"""
	Addon availability Post API

		Authentication Required		: Yes
		
		Service Usage & Description	: This Api is used to make addons available or unavailable from pos to urbanpiper.

		Data Post: {
			"is_available"  		: 		False,
			"addon_id"            	: 		"1",
			"outlet_id"        		: 		"21"
		}

		Response: {

			"success": True, 
			"message": "Addon is unavailable now!!",

		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			outlet_id = OutletProfile.objects.filter(id=data['outlet_id'], active_status=1)
			if outlet_id.count() != 0:
				pass
			else:
				return Response({
					"success"	: 	False,
					"message"	: 	"Please select valid outlet!!"
					})
			record_check = Addons.objects.filter(id=data["addon_id"],active_status=1, \
																addon_group__active_status=1)
			if record_check.count() != 0:
				pass
			else:
				return Response({
					"success"	: 	False,
					"message"	: 	"Please provide valid addon!!"
					})
			urban = OptionAction(data["addon_id"], data["outlet_id"], data["is_available"])
			if urban == None:
				return Response({
					"success" : False,
					"message" : "Item toggling is not performed well!!"
					})
			else:
				pass
			if data["is_available"] == False:
				return Response({
					"success" : True,
					"message" : "Addon is disabled at Aggregator!!"
					})
			else:
				return Response({
					"success" : True,
					"message" : "Addon is enabled at Aggregator!!"
					})
		except Exception as e:
			return Response({
				"success"	: 	False, 
				"message"	: 	"Error happened!!", "errors": str(e)
				})