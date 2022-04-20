from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Brands.models import Company
#Serializer for api
from django.db.models import Q
from urbanpiper.models import OutletSync, UrbanCred, APIReference, EventTypes, CatSync, \
ProductOutletWise,ProductSync,CatOutletWise, MenuPayload, CatOutletWise
from Outlet.models import OutletProfile
from .swiggy_sync import swiggy_menu
from .zomato_sync import zomato_menu
from .universal_sync import universal_menu
from .Menu_sync import menu_sync
from rest_framework_tracking.mixins import LoggingMixin


class UniversalSync(LoggingMixin,APIView):
	"""
	Outletwise Universal Menu Syncing POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for syncing universal menus outletwise 
		with UrbanPiper.

		Data Post: {
			"outlet_id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "Syncing of menu is initiated successfully!!"
		}
	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			data = request.data
			user = request.user.id
			query = Company.objects.filter(auth_user=user)
			if query.count() == 0:
				return Response({
					"success" 	: 	False,
					"message"	:	"You are authorized to do this operation!!"
					})
			else:
				company_id = query[0].id
			record = OutletSync.objects.filter(
									outlet=data["outlet_id"],outlet__active_status=1)
			if record.count() == 0:
				return Response({
					"status" : True,
					"message" : "Outlet is not valid to proceed!!"
					})
			else:
				company_id = record[0].company_id
				outlet_id = data["outlet_id"]
			universal_data = universal_menu(company_id, outlet_id, user)
			if  "status" not in universal_data:
				pass
			else:
				return Response (universal_data)
			urban_sync = menu_sync(universal_data,company_id, outlet_id)
			payload_create = \
			MenuPayload.objects.create(company_id=company_id,outlet_id=outlet_id, \
										payload=universal_data,plateform = "Swiggy & Zomato")
			if urban_sync != None:
				pass
			else:
				cat_revert = CatOutletWise.objects,filter(sync_outlet__outlet=outlet_id).\
				update(sync_status='not_intiated')
				product_revert =  \
				ProductOutletWise.objects,filter(sync_outlet__outlet=outlet_id).\
				update(sync_status='not_intiated')
				return Response({
							"status":False,
							"message" : "Syncing of outletwise menu is not initiated successfully!!"
							})
			return Response({
							"status":True,
							"message" : "Syncing of menu is initiated successfully!!"
							})
		except Exception as e:
			return Response(
						{"error":str(e)}
						)



class SwiggySync(LoggingMixin,APIView):
	"""
	Outletwise Swiggy Menu Syncing POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for syncing swiggy menus outletwise 
		with UrbanPiper.

		Data Post: {
			"outlet_id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "Syncing of menu is initiated successfully!!"
		}
	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			data = request.data
			user = request.user.id
			query = Company.objects.filter(auth_user=user)
			if query.count() == 0:
				return Response({
					"success" 	: 	False,
					"message"	:	"You are authorized to do this operation!!"
					})
			else:
				company_id = query[0].id
			record = OutletSync.objects.filter(sync_status='synced',\
									outlet=data["outlet_id"],outlet__active_status=1)
			if record.count() == 0:
				return Response({
					"status" : True,
					"message" : "Outlet is not valid to proceed!!"
					})
			else:
				company_id = record[0].company_id
				outlet_id = data["outlet_id"]
			swiggy_data = swiggy_menu(company_id, outlet_id, user)
			if  "status" not in swiggy_data:
				pass
			else:
				return Response (swiggy_data)
			urban_sync = menu_sync(swiggy_data,company_id, outlet_id)
			payload_create = \
			MenuPayload.objects.create(company_id=company_id,outlet_id=outlet_id, \
										payload=swiggy_data,plateform = "Swiggy")
			if urban_sync != None:
				pass
			else:
				cat_revert = CatOutletWise.objects,filter(sync_outlet__outlet=outlet_id).\
				update(sync_status='not_intiated')
				product_revert =  \
				ProductOutletWise.objects,filter(sync_outlet__outlet=outlet_id).\
				update(sync_status='not_intiated')
				return Response({
							"status":False,
							"message" : "Syncing of outletwise menu is not initiated successfully!!"
							})
			return Response({
							"status":True,
							"message" : "Syncing of menu is initiated successfully!!"
							})
		except Exception as e:
			return Response(
						{"error":str(e)}
						)


class ZomatoSync(LoggingMixin,APIView):
	"""
	Outletwise Zomato Menu Syncing POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for syncing zomato menus outletwise 
		with UrbanPiper.

		Data Post: {
			"outlet_id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "Syncing of menu is initiated successfully!!"
		}
	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			data = request.data
			user = request.user.id
			query = Company.objects.filter(auth_user=user)
			if query.count() == 0:
				return Response({
					"success" 	: 	False,
					"message"	:	"You are authorized to do this operation!!"
					})
			else:
				company_id = query[0].id
			record = OutletSync.objects.filter(
									outlet=data["outlet_id"],outlet__active_status=1)
			if record.count() == 0:
				return Response({
					"status" : True,
					"message" : "Outlet is not valid to proceed!!"
					})
			else:
				company_id = record[0].company_id
				outlet_id = data["outlet_id"]
			zomato_data = zomato_menu(company_id, outlet_id, user)
			if  "status" not in zomato_data:
				pass
			else:
				return Response (zomato_data)
			urban_sync = menu_sync(zomato_data,company_id, outlet_id)
			payload_create = \
			MenuPayload.objects.create(company_id=company_id,outlet_id=outlet_id, \
										payload=zomato_data,plateform = "Zomato")
			if urban_sync != None:
				pass
			else:
				cat_revert = CatOutletWise.objects,filter(sync_outlet__outlet=outlet_id).\
				update(sync_status='not_intiated')
				product_revert =  \
				ProductOutletWise.objects,filter(sync_outlet__outlet=outlet_id).\
				update(sync_status='not_intiated')
				return Response({
							"status":False,
							"message" : "Syncing of outletwise menu is not initiated successfully!!"
							})
			return Response({
							"status":True,
							"message" : "Syncing of menu is initiated successfully!!"
							})
		except Exception as e:
			return Response(
						{"error":str(e)}
						)


