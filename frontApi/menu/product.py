from rest_framework.views import APIView
from rest_framework.response import Response
from Product.models import ProductCategory, Product_availability, Category_availability, Product,\
Variant
from Outlet.models import OutletProfile
from Brands.models import Company
import re
from django.conf import settings
from ZapioApi.api_packages import *
from datetime import datetime
from django.db.models import Q
import random
from zapio.settings import Media_Path
from Configuration.models import TaxSetting


class FullProductList(APIView):
	"""
	Product Listing POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to extract all product associated with outlet.

		Data Post: {

			"outlet_id" : 11
		}

		Response: {

			"success": True,
			"credential" : True,
			"product_count" : product_count,
			"menu_data" : final_result
		}

	"""
	def post(self, request, format=None):
		try:
			data = request.data
			record = Product_availability.objects.filter(outlet=data["outlet_id"])
			final_result = []
			rating = [4,5,4.7,4.2]
			if record.count()!=0:
				avail_product = record[0].available_product
				if len(avail_product) != 0:
					for i in avail_product:
						query = Product.objects.filter(id=i,active_status=1)
						if query.count()!=0:
							s  = query[0]
							menu_info = {}
							menu_info["outlet_availbility_id"] = data["outlet_id"]
							menu_info["name"] = s.product_name
							menu_info["product_id"] = s.id
							menu_info["product_desc"] = s.product_desc
							menu_info["product_rating"] = random.choice(rating)
							menu_info["parent_category_id"] = s.product_category_id
							menu_info["parent_category_name"] = s.product_category.category_name
							menu_info["category_id"] = s.product_subcategory_id
							menu_info["tax_detail"] = []
							associate_tax = s.tax_association
							if associate_tax != None:
								if len(associate_tax) == 0:
									pass
								else:
									for t in associate_tax:
										tax_dict = {}
										tax_q = TaxSetting.objects.filter(id=t)[0]
										tax_dict["id"] = tax_q.id
										tax_dict["tax_name"] = tax_q.tax_name+" | "+str(tax_q.tax_percent)
										tax_dict["tax_percent"] = tax_q.tax_percent
										menu_info["tax_detail"].append(tax_dict)
							else:
								pass
							if menu_info["category_id"] != None:
								menu_info["category_name"] = \
								s.product_subcategory.subcategory_name
							else:
								menu_info["category_name"] = None
							menu_info["food_type"] = s.food_type.food_type
							if s.food_type.foodtype_image != None or s.food_type.foodtype_image != "": 
								menu_info["food_type_image"] = \
								Media_Path+str(s.food_type.foodtype_image)
							else:
								menu_info["food_type_image"] = \
								None
							if s.product_image != None and s.product_image != "":
								menu_info["product_image"] = \
								Media_Path+str(s.product_image)
							else:
								menu_info["product_image"] = \
								None
							has_variant = s.has_variant
							variant_deatils = s.variant_deatils
							if has_variant == False:
								# menu_info["costom_available"] =  False
								menu_info["price"] = s.price
								menu_info["discount"] = s.discount_price
								addon_grp = s.addpn_grp_association
								if addon_grp != None and len(addon_grp) != 0:
									is_custom = True
								else:
									is_custom = False
								menu_info["is_custom"] = is_custom
							else:
								is_custom = False
								li =[]
								li2 = []
								for j in variant_deatils:
									li.append(j["price"])
									li2.append(j["discount_price"])
									addon_grp = j["addon_group"]
									if is_custom == True:
										pass
									else:
										if len(addon_grp) != 0:
											is_custom = True
										else:
											pass
								menu_info["price"] = min(li)
								menu_info["discount"] = min(li2)
								menu_info["is_custom"] = is_custom
								menu_info["Variant_id"] = \
								Variant.objects.filter(variant__iexact=variant_deatils[0]["name"])[0].id
								menu_info["Variant_name"] = variant_deatils[0]["name"]
							final_result.append(menu_info)
						else:
							pass
				else:
					pass
			else:
				pass
			if len(final_result) != 0:
				p_count = len(final_result)
				result = {
							"success": True,
							"credential" : True,
							"product_count" : p_count,
							"menu_data" : final_result
							}
			else:
				result = {
							"success": True,
							"credential" : True
						}
			return Response(result)
		except Exception as e:
			print("Product Listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})