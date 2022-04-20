from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
#Serializer for api
from rest_framework import serializers
from django.db.models import Q
from datetime import datetime, timedelta
from urbanpiper.models import OutletSync, CatSync, CatOutletWise, SubCatSync,\
SubCatOutletWise
from Outlet.models import OutletProfile
from Product.models import ProductCategory, Product, Tag, ProductsubCategory
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user


def cat_outletwise(sync_cat_id,sync_outlet):
	query_check = CatOutletWise.objects.filter(sync_cat_id=sync_cat_id,\
										sync_outlet_id=sync_outlet)
	if query_check.count() == 0:
		query_create = \
		CatOutletWise.objects.create(sync_cat_id=sync_cat_id,\
					sync_outlet_id=sync_outlet,urban_event='created')
	else:
		pass
	return "created or updated"


def sub_cat_outletwise(sync_sub_cat_id, sync_outlet):
	query_check = SubCatOutletWise.objects.filter(sync_sub_cat=sync_sub_cat_id,\
										sync_outlet_id=sync_outlet)
	if query_check.count() == 0:
		query_create = \
		SubCatOutletWise.objects.create(sync_sub_cat_id=sync_sub_cat_id,\
					sync_outlet_id=sync_outlet,urban_event='created')
	else:
		pass
	return "created or updated"


class CatAttach(APIView):
	"""
	Outletwise attach category with urbanpiper POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for attaching categories to outlets with urbanpiper within brand.

		Data Post: {
			"outlet_id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "All categories are attached successfully!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			data = request.data
			auth_id = request.user.id
			Company_id = get_user(auth_id)
			record = OutletSync.objects.filter(outlet_id=data["outlet_id"],sync_status="synced")
			if record.count() == 0:
				return Response({
					"status" : False,
					"message" : "This outlet is not valid to proceed!!"
					})
			else:
				revert_cat_record_status = \
						CatOutletWise.objects.filter(sync_outlet__outlet=data["outlet_id"])\
									.update(sync_status='not_intiated',is_enabled=0,is_available=0,\
									updated_at=datetime.now(),urban_event=None)
				cat_q = ProductCategory.objects.filter(Company=Company_id,active_status=1)
				outlet_id = str(data["outlet_id"])
				sync_outlet = record[0].id
				for q in cat_q:
					sync_check = CatSync.objects.filter(category=q.id)
					if sync_check.count() == 0:
						outlet_map = [outlet_id]
						sync_create = CatSync.objects.create(category_id=q.id,company_id=q.Company_id,\
							outlet_map=outlet_map)
						sync_cat_id = sync_create.id
						cat_outletwise(sync_cat_id,sync_outlet)
					else:
						outlet_map = sync_check[0].outlet_map
						if outlet_id not in outlet_map:
							outlet_map.append(outlet_id)
						else:
							pass
						sync_cat_id = sync_check[0].id
						sync_update = sync_check.update(outlet_map=outlet_map)
						cat_outletwise(sync_cat_id,sync_outlet)
					sub_cat_check = \
					ProductsubCategory.objects.filter(category=q.id,active_status=1)
					if sub_cat_check.count() == 0:
						pass
					else:
						for j in sub_cat_check:
							sub_cat_sync = SubCatSync.objects.filter(sub_category=j.id)
							if sub_cat_sync.count() == 0:
								sub_outlet_map = [outlet_id]
								sync_sub_create = \
								SubCatSync.objects.create(sub_category_id=j.id, \
									company_id=q.Company_id,outlet_map= sub_outlet_map)
								sync_sub_cat_id = sync_sub_create.id
								sub_cat_outletwise(sync_sub_cat_id, sync_outlet)
							else:
								sub_outlet_map = sub_cat_sync[0].outlet_map
								if outlet_id not in sub_outlet_map:
									sub_outlet_map.append(outlet_id)
								else:
									pass
								sync_sub_cat_id = sub_cat_sync[0].id
								sync_sub_cat_update = sub_cat_sync.update(outlet_map=sub_outlet_map)
								sub_cat_outletwise(sync_sub_cat_id,sync_outlet)
				sync_count = CatOutletWise.objects.filter(sync_outlet_id=sync_outlet).count()
				if sync_count == 0:
					msg = "Categories are already attached!!"
				else:
					msg = "Total "+str(sync_count) +" categories are attached!!"
			return Response({"status": True,
							"message" : msg})
		except Exception as e:
			print(e)
			return Response(
						{"error":str(e)}
						)