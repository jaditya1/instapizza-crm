from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Brands.models import Company
#Serializer for api
from rest_framework import serializers
from django.db.models import Q
from datetime import datetime, timedelta
from urbanpiper.models import OutletSync, ActionSync, ProductSync, CatSync, CatOutletWise,\
ProductOutletWise,SubCatSync,SubCatOutletWise


class SyncedProduct(APIView):
	"""
	Products listing POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for providing attached products along with sync status with urbanpiper within brand.

		Data Post: {
			"outlet_id"                   : "1"
		}

		Response: {

			"success": True, 
			"data" : result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			user = request.user.id
			data = request.data
			record = OutletSync.objects.filter(outlet_id=data["outlet_id"],sync_status="synced",\
							outlet__active_status=1)
			if record.count() == 0:
				return Response({
					"status" : False,
					"message" : "This outlet is not valid to proceed!!"
					})
			else:
				result =[]
				product_q = ProductOutletWise.objects.filter(sync_outlet=record[0].id, \
										sync_product__product__active_status=1)
				if product_q.count() != 0:
					for i in product_q:
						record_dict ={}
						record_dict['id'] = i.id
						record_dict['p_id'] = i.sync_product_id
						variant = i.sync_product.variant
						if variant != None:
							record_dict['product'] = \
							i.sync_product.product.product_name+" | "+i.sync_product.variant.variant
						else:
							record_dict['product'] = i.sync_product.product.product_name
						record_dict['sync_status'] = i.get_sync_status_display()
						record_dict['is_synced'] = i.is_enabled
						record_dict['is_available'] = i.is_available
						record_dict['attached_at'] = \
						(i.created_at + timedelta(hours=5,minutes=30)).strftime("%d %b %y %I:%M %p")
						if i.sync_status == "not_intiated":
							color = "danger"
						elif i.sync_status == "in_progress":
							color = "warning"
						else:
							color = "success"
						record_dict["color_code"] = color
						result.append(record_dict)
				else:
					pass
				return Response({"status":True,
								"data":result})
		except Exception as e:
			print(e)
			return Response(
						{"error":str(e)}
						)


class SyncedCat(APIView):
	"""
	Category listing POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for providing attached categories along with sync status with urbanpiper within brand.

		Data Post: {
			"outlet_id"                   : "1"
		}

		Response: {

			"success": True, 
			"data" : result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			user = request.user.id
			data = request.data
			record = OutletSync.objects.filter(outlet_id=data["outlet_id"],sync_status="synced",
									outlet__active_status=1)
			if record.count() == 0:
				return ({
					"status" : False,
					"message" : "This outlet is not valid to proceed!!"
					})
			else:
				result =[]
				cat_q = CatOutletWise.objects.filter(sync_outlet=record[0].id, \
										sync_cat__category__active_status=1).order_by('priority')
				if cat_q.count() != 0:
					for i in cat_q:
						record_dict ={}
						record_dict['id'] = i.id
						record_dict["category"] = i.sync_cat.category.category_name
						record_dict['cat_id'] = i.sync_cat.category_id
						record_dict['is_synced'] = i.is_enabled
						record_dict['priority'] = i.priority
						record_dict['sync_status'] = i.get_sync_status_display()
						record_dict['is_available'] = i.is_available
						record_dict['attached_at'] = \
						(i.created_at + timedelta(hours=5,minutes=30)).strftime("%d %b %y %I:%M %p")
						if i.sync_status == "not_intiated":
							color = "danger"
						elif i.sync_status == "in_progress":
							color = "warning"
						else:
							color = "success"
						record_dict["color_code"] = color
						result.append(record_dict)
				else:
					pass
				return Response({"status":True,
								"data":result})
		except Exception as e:
			return Response(
						{"error":str(e)}
						)

class SyncedSubCat(APIView):
	"""
	Sub Category listing POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for providing attached sub-categories along with sync status with urbanpiper within brand.

		Data Post: {
			"outlet_id"                   : "1"
		}

		Response: {

			"success": True, 
			"data" : result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			user = request.user.id
			data = request.data
			record = OutletSync.objects.filter(outlet_id=data["outlet_id"],sync_status="synced",
									outlet__active_status=1)
			if record.count() == 0:
				return ({
					"status" : False,
					"message" : "This outlet is not valid to proceed!!"
					})
			else:
				result =[]
				cat_q = SubCatOutletWise.objects.filter(sync_outlet=record[0].id, \
								sync_sub_cat__sub_category__active_status=1).order_by('priority')
				if cat_q.count() != 0:
					for i in cat_q:
						record_dict ={}
						record_dict['id'] = i.id
						record_dict["subcategory"] = i.sync_sub_cat.sub_category.subcategory_name
						record_dict['subcat_id'] = i.sync_sub_cat.sub_category_id
						record_dict['is_synced'] = i.is_enabled
						record_dict['priority'] = i.priority
						record_dict['sync_status'] = i.get_sync_status_display()
						record_dict['is_available'] = i.is_available
						record_dict['attached_at'] = \
						(i.created_at + timedelta(hours=5,minutes=30)).strftime("%d %b %y %I:%M %p")
						if i.sync_status == "not_intiated":
							color = "danger"
						elif i.sync_status == "in_progress":
							color = "warning"
						else:
							color = "success"
						record_dict["color_code"] = color
						result.append(record_dict)
				else:
					pass
				return Response({"status":True,
								"data":result})
		except Exception as e:
			print(e)
			return Response(
						{"error":str(e)}
						)