from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from Product.models import Product, Product_availability, Category_availability, ProductCategory
from ZapioApi.api_packages import *
import re
from ZapioApi.Api.BrandApi.outletmgmt.availability.available import *
from ZapioApi.Api.urbanpiper.sync.item_action import SingleItemAction
from rest_framework_tracking.mixins import LoggingMixin
from urbanpiper.models import ProductSync
from Outlet.models import OutletProfile
from _thread import start_new_thread
from PosApi.Api.outletmgmt.outletwiselisting.available import MenuSync




class PosLevelVariantavail(LoggingMixin,APIView):
	"""
	Varaint availability Post API

		Authentication Required		: Yes
		
		Service Usage & Description	: This Api is used to make variants available or unavailable from pos to urbanpiper.

		Data Post: {
			"is_available"  	: 	False,
			"p_id"            	: 	"1",
			"v_id"				:	"28",
			"outlet_id"        	: 	"21"
		}

		Response: {

			"success": True, 
			"message": "Product is unavailable now!!",

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
			record_check = ProductSync.objects.filter(product=data["p_id"],variant=data["v_id"],\
											active_status=1)
			if record_check.count() != 0:
				pass
			else:
				return Response({
					"success"	: 	False,
					"message"	: 	"Please provide valid product and variant!!"
					})
			p_id = record_check[0].id
			urban = SingleItemAction(p_id, data["outlet_id"], data["is_available"])
			if urban == None:
				return Response({
					"success" : False,
					"message" : "Item toggling is not performed well!!"
					})
			else:
				pass
			cache_sync = {}
			cache_sync["outlet"] = data["outlet_id"]
			start_new_thread(MenuSync, (cache_sync,))
			if data["is_available"] == False:
				return Response({
					"success" : True,
					"is_available" : data["is_available"],
					"message" : "Requested to portal, sync menu in progress, visit this again after some time!!"
					})
			else:
				return Response({
					"success" : True,
					"is_available" : data["is_available"],
					"message" : "Requested to portal, sync menu in progress, visit this again after some time!!"
					})
		except Exception as e:
			return Response({
				"success"	: 	False, 
				"message"	: 	"Error happened!!", "errors": str(e)
				})