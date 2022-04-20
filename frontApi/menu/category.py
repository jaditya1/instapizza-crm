from rest_framework.views import APIView
from rest_framework.response import Response
from Product.models import ProductCategory, Product_availability, Category_availability,ProductsubCategory
from Outlet.models import OutletProfile
from Brands.models import Company
import re
from django.conf import settings
from ZapioApi.api_packages import *
from datetime import datetime
from django.db.models import Q



class CatListing(APIView):
	"""
	Catogery Listing POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to extract all product category within outlet.

		Data Post: {
			"outlet_id" : 11
		}

		Response: {

			"success": True,
			"credential" : True,
			"cat_count" : cat_count,
			"cat_data" : Cat_serializer
		}

	"""
	def post(self, request, format=None):
		try:
			data = request.data
			record = Category_availability.objects.filter(outlet=data["outlet_id"])
			Cat_serializer = []
			if record.count()!=0:
				avail_cat = record[0].available_cat
				if len(avail_cat) != 0:
					for i in avail_cat:
						query = ProductCategory.objects.filter(id=i,active_status=1)
						if query.count() != 0 :
							cat_info = {}
							cat_info["c_id"] = query[0].id
							cat_info["category_name"] = query[0].category_name
							cat_info["ordering"] = query[0].priority

							query1 = ProductsubCategory.objects.filter(category = cat_info["c_id"],active_status=1)
							cat_info1 = []
							for i in query1:
								sub_cat = {}
								sub_cat["sub_c_id"] = i.id
								sub_cat["sub_category_name"] = i.subcategory_name
								sub_cat["sub_ordering"] = i.priority
								cat_info1.append(sub_cat)
							cat_info["sub_cat_detail"] = cat_info1
							Cat_serializer.append(cat_info)
						else:
							pass
				else:
					pass
			else:
				pass
			if len(Cat_serializer) != 0:
				cat_count = len(Cat_serializer)
				result = {
							"success": True,
							"credential" : True,
							"cat_count" : cat_count,
							"cat_data" : Cat_serializer
							}
			else:
				result = {
							"success": True,
							"credential" : True
						}
			return Response(result)
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})