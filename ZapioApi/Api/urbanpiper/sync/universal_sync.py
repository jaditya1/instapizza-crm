from Brands.models import Company
#Serializer for api
from rest_framework import serializers
from django.db.models import Q
from datetime import datetime, timedelta
from urbanpiper.models import OutletSync, UrbanCred, APIReference, EventTypes, CatSync, \
ProductOutletWise,ProductSync,CatOutletWise, MenuPayload, CatOutletWise
from Outlet.models import OutletProfile
from datetime import datetime, timedelta
import requests
import json
from zapio.settings import Media_Path
from Product.models import Variant, AddonDetails, Addons, Tag
from Configuration.models import DeliverySetting, TaxSetting
from rest_framework.response import Response
from Product.models import ProductsubCategory

def universal_menu(company_id, outlet_id, user):
	sync_data = {}
	sync_data["flush_items"] = False
	sync_data["flush_options"] = False
	sync_data["flush_option_groups"] = False
	sync_data["categories"] = []
	sync_data["items"] = []
	sync_data["option_groups"] = []
	sync_data["options"] = []
	sync_data["taxes"] = []
	sync_data["charges"] = []
	cat_q = CatSync.objects.filter(category__active_status=1,company=company_id)
	if cat_q.count() == 0:
		error = {
			"status":False,
			"message" : "No categories are attached!!"
			}
		return error
	else:
		cat_ids = []
		for q in cat_q:
			cat_dict = {}
			cat_dict["ref_id"] = "C-"+str(q.category_id)
			cat_dict["name"] = q.category.category_name
			cat_dict["description"] = q.category.description
			outletwise_cat = CatOutletWise.objects.filter(sync_outlet__outlet=outlet_id,\
										sync_cat=q.id)
			if outletwise_cat.count() == 0:
				error = {
					"status" : False,
					"message" : "Outletwise category not found!!"
					}
				return error
			else:
				sort_order = outletwise_cat[0].priority
			if sort_order == None:
				sort_order = 0
			else:
				pass
			cat_dict["sort_order"] = sort_order
			cat_dict["active"] = True
			cat_dict["img_url"] = None
			cat_dict["parent_ref_id"] = None
			sync_data["categories"].append(cat_dict)
			if q.category_id not in cat_ids:
				cat_ids.append(q.category_id)
			else:
				pass
			cat_update = CatOutletWise.objects.\
			filter(sync_cat=q.id,sync_outlet__outlet=outlet_id).\
			update(sync_status="in_progress")
			
		#For subcategory
		for i in cat_ids:
			sub_q = ProductsubCategory.objects.filter(category=i,active_status=1)
			if sub_q.count() != 0:
				for x in sub_q:
					subcat_dict = {}
					subcat_dict["ref_id"] = "SC-"+str(x.id)
					subcat_dict["name"] = x.subcategory_name
					subcat_dict["description"] = None
					subcat_dict["sort_order"] = None
					subcat_dict["active"] = True
					subcat_dict["img_url"] = None
					subcat_dict["parent_ref_id"] = "C-"+str(i)
					sync_data["categories"].append(subcat_dict)
			else:
				pass



	product_q = ProductSync.objects.filter(product__active_status=1, \
								company__auth_user=user,active_status=1)
	# cid = product_q[0].company_id
	if product_q.count() == 0:
		error = {
			"status":False,
			"message" : "No products are attached for universal menu push!!"
			}
		return error
	else:
		item_ids = []
		addon_grp = []
		for i in product_q:
			if i.price != 0.0 and i.product.included_platform != None and \
			len(i.product.included_platform) != 0:
				product_dict = {}
				product_dict["ref_id"] = "I-"+str(i.id) 
				item_ids.append(product_dict["ref_id"])
				product_dict["title"] = i.product.product_name
				if i.variant == None:
					pass
				else:
					product_dict["title"] = i.product.product_name + " | " + i.variant.variant  
				product_dict["price"] = i.price
				product_dict["description"] = i.product.product_desc
				product_dict["sold_at_store"] = True
				product_dict["available"] = True
				product_dict["sort_order"] = i.product.priority
				product_dict["current_stock"] = -1
				product_dict["category_ref_ids"] = []
				# product_dict["category_ref_ids"].append("C-"+str(i.category_id))
				if i.product.product_subcategory_id == None:
					product_dict["category_ref_ids"].append("C-"+str(i.category_id))
				else:
					final_subcat_id = "SC-"+str(i.product.product_subcategory_id)
					product_dict["category_ref_ids"].append(final_subcat_id)
				product_dict["food_type"] = i.product.food_type.food_type
				if product_dict["food_type"] == "Vegetarian":
					product_dict["food_type"] = 1
				else:
					product_dict["food_type"] = 2
				product_dict['img_url'] = i.product.product_image
				if product_dict['img_url'] != None and product_dict['img_url'] != "" and\
					product_dict['img_url'] != "null":
					product_dict['img_url'] = Media_Path+str(i.product.product_image)
				else:
					product_dict['img_url'] = None
				product_dict["recommended"] = i.product.is_recommended
				product_dict["translations"] = []
				product_dict["language"] = []
				product_dict["tags"] = {}
				zomato_tags = []
				swiggy_tags = []
				if i.product.tags != None and len(i.product.tags)!=0:
					tag_ids = i.product.tags
					for j in tag_ids:
						tag_rec = Tag.objects.filter(id=j)
						if tag_rec.count()!= 0:
							tag_name = tag_rec[0].tag_name
							zomato_tags.append(tag_name)
							swiggy_tags.append(tag_name)
						else:
							pass
				else:
					pass
				if len(zomato_tags)!=0:
					product_dict["tags"]["zomato"] = zomato_tags
				else:
					pass
				if len(swiggy_tags) != 0:
					product_dict["tags"]["swiggy"] = swiggy_tags
				else:
					pass
				product_dict["excluded_platforms"] = []
				product_dict["included_platforms"] = i.product.included_platform
				sync_data["items"].append(product_dict)
				product_update = ProductOutletWise.objects.\
				filter(sync_product=i.id,sync_outlet__outlet=outlet_id).\
				update(sync_status="in_progress")
				associate_addon_grp = i.addpn_grp_association
				for j in  associate_addon_grp:
					if j not in addon_grp:
						addon_group = AddonDetails.objects.filter(active_status=1,\
							Company_id=company_id,id=str(j))
						if addon_group.count() != 0:
							addon_grp.append(j)
						else:
							pass
					else:
						pass
			else:
				pass

	addon_grp_q = AddonDetails.objects.filter(active_status=1,Company_id=company_id)
	for k in addon_grp_q:
		product_check = product_q.filter(addpn_grp_association__contains=[str(k.id)])
		if product_check.count() != 0:
			addon_grp_dict = {}
			query = addon_grp_q.filter(id=k.id)[0]
			if query.associated_addons != None and len(query.associated_addons) != 0: 
				addon_grp_dict["ref_id"] = "AG-"+str(query.id)
				addon_grp_dict["title"] = query.addon_gr_name
				addon_grp_dict["description"] = None
				addon_grp_dict["min_selectable"] = query.min_addons
				addon_grp_dict["max_selectable"] = query.max_addons
				addon_grp_dict["sort_order"] = 0
				addon_grp_dict["active"] = True
				addon_grp_dict["display_inline"] = True
				addon_grp_dict["item_ref_ids"] = []
				for l in product_check:
					item_id = "I-"+str(l.id) 
					if item_id not in addon_grp_dict["item_ref_ids"]:
						addon_grp_dict["item_ref_ids"].append(item_id)
					else:
						pass
				addon_grp_dict["translations"] = []
				addon_grp_dict["language"] = []
				sync_data["option_groups"].append(addon_grp_dict)
			else:
				pass
		else:
			pass
	for m in addon_grp:
		addon_q = Addons.objects.filter(active_status=1,addon_group_id=m)
		for n in addon_q:
			addon_dict = {}
			addon_dict["ref_id"] = "A-"+str(n.id)
			addon_dict["title"] = n.name
			addon_dict["price"] = n.addon_amount
			addon_dict["description"] = None
			addon_dict["available"] = True
			addon_dict["sold_at_store"] = True
			addon_dict["food_type"] = 1
			addon_dict["translations"] = []
			addon_dict["opt_grp_ref_ids"] = []
			addon_dict["opt_grp_ref_ids"].append("AG-"+str(m))
			addon_dict["nested_opt_grps"] = []
			addon_dict["language"] = []
			sync_data["options"].append(addon_dict)

	return sync_data