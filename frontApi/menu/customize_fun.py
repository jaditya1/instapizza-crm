from rest_framework.views import APIView
from rest_framework.response import Response
from Product.models import ProductCategory, Product_availability, Category_availability, Product,\
Variant,AddonDetails
from Outlet.models import OutletProfile
from Brands.models import Company
import re
from django.conf import settings
from ZapioApi.api_packages import *
from datetime import datetime
from django.db.models import Q
import random
from zapio.settings import Media_Path
from Product.models import Addons
from urbanpiper.models import ProductSync, ProductOutletWise


def addon_manage(addon_grp,add_on_list):
	if len(addon_grp) != 0:
		for k in addon_grp:
			addon_q = AddonDetails.objects.filter(active_status=1,id=k)
			if addon_q.count() != 0:
				addon_dict = {}
				q = addon_q[0]
				addon_dict["addon_grp_id"] = q.id
				addon_dict["add_on_group_name"] = q.addon_gr_name
				addon_dict["max_choice"] = q.max_addons
				addon_dict["min_choice"] = q.min_addons
				addon_dict["description"] = q.description
				addon_dict["add_ons"] = []
				associated_addons = q.associated_addons
				if associated_addons != None and associated_addons != "" and\
						len(associated_addons)!=0:
					for l in associated_addons:
						addons_wise_dict = {}
						l["addon_name"] = l["addon_name"].strip()
						addon_q = \
						Addons.objects.filter(name__iexact=l["addon_name"],addon_amount=l["price"],\
										addon_group__addon_gr_name=addon_dict["add_on_group_name"])
						if addon_q.count() != 0:
							addons_wise_dict["addon_id"] = addon_q[0].id
							if "priority" in l:
								addons_wise_dict["priority"] = l["priority"]
							else:
								addons_wise_dict["priority"] = "N/A"
						else:
							addons_wise_dict["addon_id"] = "N/A"
							addons_wise_dict["priority"] = "N/A"
						addons_wise_dict["addon_name"] = l["addon_name"]
						addons_wise_dict["price"] = l["price"]
						addon_dict["add_ons"].append(addons_wise_dict)
				else:
					pass
				add_on_list.append(addon_dict)
			else:
				pass
	else:
		pass
	return add_on_list


def CustomizeProduct(data):
	record = Product.objects.filter(id=data["p_id"],active_status=1)
	final_result = []
	if record.count() != 0:
		s = record[0]
		customize_info = {}
		customize_info["name"] = s.product_name
		customize_info["id"] = s.id
		customize_info["sub_description"] = s.product_desc
		customize_info["food_type"] = s.food_type.food_type
		customize_info["food_type_image"] = \
		Media_Path+str(s.food_type.foodtype_image)
		customize_info["image_link"] = \
		Media_Path+str(s.product_image)
		final_result.append(customize_info)
		customize_info["groups"] = []
		if s.has_variant == True:
			is_custom = False
			variant_detail = s.variant_deatils
			for j in variant_detail:
				v_size = {}
				v_size["name"] = "Size"
				v_size["min"] = 1
				v_size["max"] = 1
				v_size["products"] = {}
				v_size["products"]["product_name"] = j["name"]
				
				v_size["products"]["variant_id"] = \
				Variant.objects.filter(variant__iexact=j["name"])[0].id
				if "outlet" in data:
					up_record = \
					ProductOutletWise.objects.filter(sync_product__product=s.id,\
						sync_product__variant=v_size["products"]["variant_id"],\
										sync_product__active_status=1,sync_outlet__outlet=data["outlet"])
					if up_record.count()==0:
						v_size["products"]["is_available"] = "N/A"
					else:
						v_size["products"]["is_available"] = up_record[0].is_available
				else:
					pass
				v_size["products"]["price"] = j["price"]
				v_size["products"]["discount"] = j["discount_price"]
				v_size["products"]["add_on_groups"] = []
				addon_grp = j["addon_group"]
				if is_custom == True:
					pass
				else:
					if len(addon_grp) != 0:
						is_custom = True
					else:
						pass
				addon_manage_list = addon_manage(addon_grp,v_size["products"]["add_on_groups"])
				v_size["products"]["add_on_groups"] = addon_manage_list
				customize_info["groups"].append(v_size)
		else:
			addon_grp = s.addpn_grp_association
			if addon_grp != None and len(addon_grp) != 0:
				is_custom = True
			else:
				is_custom = True
			v_size = {}
			v_size["products"] = {}
			v_size["products"]["add_on_groups"] = []
			addon_manage_list = addon_manage(addon_grp,v_size["products"]["add_on_groups"])
			v_size["products"]["add_on_groups"] = addon_manage_list
			customize_info["groups"].append(v_size)
	else:
		pass
	if len(final_result) != 0:
		costom_available = True
		result = {
					"success"			: 	True,
					"credential" 		: 	True,
					"customize_data" 	: 	final_result,
					"costom_available" 	: 	costom_available,
					"is_custom"			:	is_custom
					}
	else:
		costom_available = False
		result = {
					"success"			: 	True,
					"credential" 		: 	True,
					"costom_available" 	: 	costom_available,
					"is_custom"			:	is_custom
				}
	return result