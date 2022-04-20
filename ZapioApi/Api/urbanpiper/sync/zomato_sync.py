from Brands.models import Company
#Serializer for api
from rest_framework import serializers
from django.db.models import Q
from datetime import datetime, timedelta
from urbanpiper.models import OutletSync, UrbanCred, APIReference, EventTypes, CatSync, \
ProductOutletWise,ProductSync,CatOutletWise, MenuPayload, CatOutletWise, \
zomatoMenuTemporaryAddonData, zomatoMenuTemporaryItemData, zomatoMenuTempOptionData,\
zomatoMenuTempAddonGrpData, zomatoMenuTempAllAddonData
from Outlet.models import OutletProfile
from datetime import datetime, timedelta
import requests
import json
from zapio.settings import Media_Path
from Product.models import Variant, AddonDetails, Addons, Tag
from Configuration.models import DeliverySetting, TaxSetting
from rest_framework.response import Response
from Product.models import ProductsubCategory


def add_on_grp_sort(addon_group):
	if "Crust" in addon_group:
		sort_order = 1
	elif "Cheese" in addon_group:
		sort_order = 2
	elif "Non" in addon_group:
		sort_order = 3
	elif "Vegetarian" in addon_group:
		sort_order = 4
	else:
		sort_order = 5
	return sort_order


def zomato_menu(company_id, outlet_id, user):
	zomatoMenuTempAllAddonData.objects.all().delete()
	zomatoMenuTemporaryAddonData.objects.all().delete()
	zomatoMenuTemporaryItemData.objects.all().delete()
	zomatoMenuTempOptionData.objects.all().delete()
	zomatoMenuTempAddonGrpData.objects.all().delete()
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
		return Response({
			"status":False,
			"message" : "No categories are attached for zomato menu push!!"
			})
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
			# cat_dict["img_url"] = None
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
					# subcat_dict["description"] = None
					# subcat_dict["sort_order"] = None
					subcat_dict["active"] = True
					# subcat_dict["img_url"] = None
					subcat_dict["parent_ref_id"] = "C-"+str(i)
					sync_data["categories"].append(subcat_dict)
			else:
				pass
	product_q = ProductSync.objects.filter(product__active_status=1, \
								company__auth_user=user,active_status=1)
	if product_q.count() == 0:
		error = {
			"status":False,
			"message" : "No products are attached!!"
			}
		return error
	else:
		ketchup_ref_ids = []
		for i in product_q:
			if i.price != 0.0 and i.product.included_platform != None and\
				"zomato" in i.product.included_platform:
				if i.variant == None:
					ref_id = "ZI-"+str(i.id)
					if "104" in i.addpn_grp_association:
						if ref_id not in ketchup_ref_ids:
							ketchup_ref_ids.append(ref_id)
						else:
							pass
					else:
						pass
				else:
					ref_id = "Z-MI-"+str(i.product_id)
					if "104" in i.addpn_grp_association:
						if ref_id not in ketchup_ref_ids:
							ketchup_ref_ids.append(ref_id)
						else:
							pass
					else:
						pass
			else:
				pass

		all_p_id_with_variant = []
		for i in product_q:
			if i.price != 0.0 and i.product.included_platform != None and\
				"zomato" in i.product.included_platform:
				product_dict = {}
				if i.variant == None:
					product_dict["ref_id"] = "ZI-"+str(i.id)
					product_dict["price"] = i.price
					product_dict["title"] = i.product.product_name
					product_dict["description"] = i.product.product_desc
					product_dict["sold_at_store"] = True
					product_dict["available"] = True
					product_dict["sort_order"] = i.product.priority
					product_dict["current_stock"] = -1
					product_dict["category_ref_ids"] = []
					if i.product.product_subcategory_id == None:
						product_dict["category_ref_ids"].append("C-"+str(i.category_id))
					else:
						final_subcat_id = "SC-"+str(i.product.product_subcategory_id)
						product_dict["category_ref_ids"].append(final_subcat_id)
					# product_dict["category_ref_ids"].append("C-"+str(i.category_id))
					product_dict["food_type"] = i.product.food_type.food_type
					if product_dict["food_type"] == "Vegetarian":
						product_dict["food_type"] = 1
					else:
						product_dict["food_type"] = 2
					img_url = i.product.product_image
					if img_url != None and img_url != "" and\
						img_url != "null":
						product_dict['img_url'] = Media_Path+str(img_url)
					else:
						# product_dict['img_url'] = None
						pass
					product_dict["recommended"] = i.product.is_recommended
					# product_dict["translations"] = []
					# product_dict["language"] = []
					product_dict["tags"] = {}
					zomato_tags = []
					if i.product.tags != None and len(i.product.tags)!=0:
						tag_ids = i.product.tags
						for j in tag_ids:
							tag_rec = Tag.objects.filter(id=j)
							if tag_rec.count()!= 0:
								tag_name = tag_rec[0].tag_name
								zomato_tags.append(tag_name)
							else:
								pass
					else:
						pass
					if len(zomato_tags) != 0:
						product_dict["tags"]["zomato"] = zomato_tags
					else:
						pass
					product_dict["excluded_platforms"] = ["swiggy"]
					product_dict["included_platforms"] = ["zomato"]
					sync_data["items"].append(product_dict)
					for j in i.addpn_grp_association:
						if j == "104":
							pass
						else:
							product_check = product_q.filter(addpn_grp_association__contains=[str(j)])
							addon_grp_q = \
							AddonDetails.objects.filter(active_status=1,id=j)
							if addon_grp_q.count()==0:
								pass
							else:
								query = addon_grp_q[0]
								zomato_addon_grp_id = "AG-"+str(query.id)
								temp_addon_data = \
									zomatoMenuTempAddonGrpData.objects.\
									filter(zomato_addon_grp_id=zomato_addon_grp_id)
								if temp_addon_data.count()==0:
									addon_grp_dict = {}
									if query.associated_addons != None and \
												len(query.associated_addons) != 0: 
										addon_grp_dict["ref_id"] = "AG-"+str(query.id)
										addon_grp_dict["title"] = query.addon_gr_name
										# addon_grp_dict["description"] = None
										addon_grp_dict["min_selectable"] = query.min_addons
										addon_grp_dict["max_selectable"] = query.max_addons
										addon_grp_dict["sort_order"] = 0
										addon_grp_dict["active"] = True
										addon_grp_dict["display_inline"] = False
										addon_grp_dict["item_ref_ids"] = []
										for l in product_check:
											item_id = "ZI-"+str(l.id) 
											if item_id not in addon_grp_dict["item_ref_ids"]:
												addon_grp_dict["item_ref_ids"].append(item_id)
											else:
												pass
										# addon_grp_dict["description"] = None
										# addon_grp_dict["translations"] = []
										# addon_grp_dict["language"] = []
										sync_data["option_groups"].append(addon_grp_dict)
									else:
										pass
									temp_addon_data_create = \
									zomatoMenuTempAddonGrpData.objects.\
										create(zomato_addon_grp_id=zomato_addon_grp_id)
								else:
									pass

					for m in i.addpn_grp_association:
						if "104" in i.addpn_grp_association:
							pass
						else:
							addon_q = Addons.objects.filter(active_status=1,addon_group_id=m,\
																	addon_group__active_status=1)
							for n in addon_q:
								temp_alladdon_data = \
								zomatoMenuTempAllAddonData.objects.filter(zomato_addon_grp_id=\
										"AG-"+str(m),zomato_addon_id="A-"+str(n.id))
								if temp_alladdon_data.count()==0:
									addon_dict = {}
									addon_dict["ref_id"] = "A-"+str(n.id)
									addon_dict["title"] = \
									n.name +"  | "+n.addon_group.product_variant.variant
									addon_dict = {}
									addon_dict["ref_id"] = "A-"+str(n.id)
									addon_dict["title"] = n.name
									addon_dict["price"] = n.addon_amount
									# addon_dict["description"] = None
									addon_dict["available"] = True
									addon_dict["sold_at_store"] = True
									addon_dict["food_type"] = 1
									# addon_dict["translations"] = []
									addon_dict["opt_grp_ref_ids"] = []
									addon_dict["opt_grp_ref_ids"].append("AG-"+str(m))
									addon_dict["nested_opt_grps"] = []
									# addon_dict["language"] = []
									sync_data["options"].append(addon_dict)
									temp_alladdon_create = \
									zomatoMenuTempAllAddonData.objects.create(zomato_addon_grp_id=\
										"AG-"+str(m),zomato_addon_id="A-"+str(n.id))
								else:
									pass
				else:
					ref_id = "Z-MI-"+str(i.product_id)
					temp_itemdata = \
					zomatoMenuTemporaryItemData.objects.filter(zomato_product_id=ref_id)
					if temp_itemdata.count() == 0:
						product_dict["ref_id"] = ref_id
						product_dict["price"] = 0
						product_dict["title"] = i.product.product_name
						product_dict["description"] = i.product.product_desc
						product_dict["sold_at_store"] = True
						product_dict["available"] = True
						product_dict["sort_order"] = i.product.priority
						product_dict["current_stock"] = -1
						product_dict["category_ref_ids"] = []
						if i.product.product_subcategory_id == None:
							product_dict["category_ref_ids"].append("C-"+str(i.category_id))
						else:
							final_subcat_id = "SC-"+str(i.product.product_subcategory_id)
							product_dict["category_ref_ids"].append(final_subcat_id)
						# product_dict["category_ref_ids"].append("C-"+str(i.category_id))
						product_dict["food_type"] = i.product.food_type.food_type
						if product_dict["food_type"] == "Vegetarian":
							product_dict["food_type"] = 1
						else:
							product_dict["food_type"] = 2
						img_url = i.product.product_image
						if img_url != None and img_url != "" and\
							img_url != "null":
							product_dict['img_url'] = Media_Path+str(img_url)
						else:
							# product_dict['img_url'] = None
							pass
						product_dict["recommended"] = i.product.is_recommended
						# product_dict["translations"] = []
						# product_dict["language"] = []
						product_dict["tags"] = {}
						zomato_tags = []
						if i.product.tags != None and len(i.product.tags)!=0:
							tag_ids = i.product.tags
							for j in tag_ids:
								tag_rec = Tag.objects.filter(id=j)
								if tag_rec.count()!= 0:
									tag_name = tag_rec[0].tag_name
									zomato_tags.append(tag_name)
								else:
									pass
						else:
							pass
						if len(zomato_tags) != 0:
							product_dict["tags"]["zomato"] = zomato_tags
						else:
							pass
						product_dict["excluded_platforms"] = ["swiggy"]
						product_dict["included_platforms"] = ["zomato"]
						sync_data["items"].append(product_dict)
						temp_itemdata_create = \
						zomatoMenuTemporaryItemData.objects.create(zomato_product_id=ref_id)
					else:
						pass


					product_id_q = \
					product_q.filter(product=i.product_id)[0]
					final_id = "CV-"+str(product_id_q.id)

					

					temp_final_itemdata = \
					zomatoMenuTemporaryItemData.objects.filter(is_size=1, \
									zomato_product_id=final_id)
					if temp_final_itemdata.count() == 0:
						variant_dict = {}
						variant_dict["ref_id"] = final_id
						variant_dict["title"] = "Choose Your Size"
						# variant_dict["description"] = None
						variant_dict["sort_order"] = 0
						variant_dict["min_selectable"] = 1
						variant_dict["max_selectable"] = 1
						variant_dict["active"] = True
						variant_dict["display_inline"] = False
						variant_dict["item_ref_ids"] = []
						variant_dict["item_ref_ids"].append(ref_id)
						# variant_dict["translations"] = []
						# variant_dict["language"] = []
						sync_data["option_groups"].append(variant_dict)
						temp_final_itemdata_create = \
						zomatoMenuTemporaryItemData.objects.create(zomato_product_id=final_id,\
												is_size=1)
					else:
						final_id = temp_final_itemdata[0].zomato_product_id


					if "104" in i.addpn_grp_association:
						temp_Ketchup = \
						zomatoMenuTemporaryAddonData.objects.filter(addon_grp="AG-104") 
						if temp_Ketchup.count() == 0:
							Ketchup_dict = {}
							Ketchup_dict["ref_id"] = "AG-104"
							Ketchup_dict["title"] = "Ketchup"
							Ketchup_dict["description"] = "Ketchup for all sizes"
							Ketchup_dict["item_ref_ids"] = ketchup_ref_ids
							# Ketchup_dict["item_ref_ids"].append(ref_id)
							# Ketchup_dict["translations"] = []
							# Ketchup_dict["language"] = []
							Ketchup_dict["min_selectable"] = 1
							Ketchup_dict["max_selectable"] = 3
							Ketchup_dict["sort_order"] = 7
							Ketchup_dict["active"] = True
							Ketchup_dict["display_inline"] = False
							sync_data["option_groups"].append(Ketchup_dict)
							temp_create = \
							zomatoMenuTemporaryAddonData.objects.create(addon_grp="AG-104")
						else:
							pass
					else:
						pass
	
					for j in i.addpn_grp_association:
						if j == "104":
							pass
						else:
							addon_grp_q = \
								AddonDetails.objects.filter(active_status=1,id=j,is_crust=0)
							if addon_grp_q.count()==0:
								pass
							else:
								query = addon_grp_q[0]
								zomato_addon_grp_id = "AG-"+str(query.id)
								temp_addon_data = \
								zomatoMenuTempAddonGrpData.objects.\
								filter(zomato_addon_grp_id=zomato_addon_grp_id)
								if temp_addon_data.count() == 0:
									addon_grp_dict = {}
									if query.associated_addons != None and \
												len(query.associated_addons) != 0: 
										addon_grp_dict["ref_id"] = "AG-"+str(query.id)
										addon_grp_dict["title"] = \
										query.addon_gr_name
										# addon_grp_dict["description"] = None
										addon_grp_dict["min_selectable"] = query.min_addons
										addon_grp_dict["max_selectable"] = query.max_addons
										addon_grp_dict["sort_order"] = \
										add_on_grp_sort(addon_grp_dict["title"])
										addon_grp_dict["active"] = True
										addon_grp_dict["display_inline"] = False
										addon_grp_dict["item_ref_ids"] = []
										# addon_grp_dict["translations"] = []
										# addon_grp_dict["language"] = [] 
										sync_data["option_groups"].append(addon_grp_dict)
									else:
										pass
									temp_addon_data_create = \
									zomatoMenuTempAddonGrpData.objects.\
										create(zomato_addon_grp_id=zomato_addon_grp_id)
								else:
									pass



					if 	i.zomato_crust_id != None:
						zomato_crust_id = i.zomato_crust_id_id
						final_zomato_crust_id = "AG-"+str(zomato_crust_id)
						temp_addongrp_data = \
								zomatoMenuTempAddonGrpData.objects.\
								filter(zomato_addon_grp_id=final_zomato_crust_id)
						if temp_addongrp_data.count() == 0:
							addon_grp_dict = {}
							addon_grp_dict["ref_id"] = final_zomato_crust_id
							addon_grp_dict["title"] = \
							i.zomato_crust_id.addon_gr_name
							# addon_grp_dict["description"] = None
							addon_grp_dict["min_selectable"] = i.zomato_crust_id.min_addons
							addon_grp_dict["max_selectable"] = i.zomato_crust_id.max_addons
							addon_grp_dict["sort_order"] = \
							add_on_grp_sort(addon_grp_dict["title"])
							addon_grp_dict["active"] = True
							addon_grp_dict["display_inline"] = False
							addon_grp_dict["item_ref_ids"] = []
							# addon_grp_dict["translations"] = []
							# addon_grp_dict["language"] = [] 
							sync_data["option_groups"].append(addon_grp_dict)
							temp_addongrp_data_create = \
							zomatoMenuTempAddonGrpData.objects.\
								create(zomato_addon_grp_id=final_zomato_crust_id)
						else:
							pass
					else:
						pass



					opt_id = "OPT-"+str(i.id)

					if i.id in all_p_id_with_variant:
						pass
					else:
						all_p_id_with_variant.append(i.id)

					temp_opt_data = \
					zomatoMenuTempOptionData.objects.filter(zomato_product_id=opt_id)
					if temp_opt_data.count() == 0 and i.zomato_crust_id!=None:
						opt_variant_dict = {}
						opt_variant_dict["ref_id"] = opt_id
						opt_variant_dict["title"] = i.product.product_name+" | "+i.variant.variant
						opt_variant_dict["price"] = i.price
						# opt_variant_dict["description"] = None
						opt_variant_dict["available"] = True
						opt_variant_dict["sold_at_store"] = True
						opt_variant_dict["food_type"] = i.product.food_type.food_type
						if opt_variant_dict["food_type"] == "Vegetarian":
							opt_variant_dict["food_type"] = 1
						else:
							opt_variant_dict["food_type"] = 2
						# opt_variant_dict["translations"] = []
						opt_variant_dict["opt_grp_ref_ids"] = []
						opt_variant_dict["opt_grp_ref_ids"].append(final_id)
						opt_variant_dict["nested_opt_grps"] = []
						level_1_crust = "AG-"+str(i.zomato_crust_id_id)
						opt_variant_dict["nested_opt_grps"].append(level_1_crust)
						opt_variant_dict["language"] = []
						sync_data["options"].append(opt_variant_dict)
						temp_opt_data_create = \
						zomatoMenuTempOptionData.objects.create(zomato_product_id=opt_id)
					else:
						pass

					if 	i.zomato_crust_id != None:
						zomato_crust_id = i.zomato_crust_id_id
						addons = Addons.objects.filter(active_status=1,addon_group_id=zomato_crust_id)
						for l in addons:
							temp_alladdon_crust_data = \
							zomatoMenuTempAllAddonData.objects.filter(zomato_addon_grp_id=\
										"AG-"+str(zomato_crust_id),zomato_addon_id="A-"+str(l.id))
							if temp_alladdon_crust_data.count()==0:
								addon_dict = {}
								addon_dict["ref_id"] = "A-"+str(l.id)
								addon_dict["title"] = l.name
								addon_dict["price"] = l.addon_amount
								# addon_dict["description"] = None
								addon_dict["available"] = True
								addon_dict["sold_at_store"] = True
								addon_dict["food_type"] = 1
								# addon_dict["translations"] = []
								addon_dict["opt_grp_ref_ids"] = []
								addon_dict["opt_grp_ref_ids"].append("AG-"+str(zomato_crust_id))
								addon_dict["nested_opt_grps"] = []
								nested = l.addon_group.zomato_nested_crusts
								for m in nested:
									addon_dict["nested_opt_grps"].append("AG-"+str(m))
								sync_data["options"].append(addon_dict)
								temp_alladdon_small_crust_data_create = \
								zomatoMenuTempAllAddonData.objects.create(zomato_addon_grp_id=\
									"AG-"+str(zomato_crust_id),zomato_addon_id="A-"+str(l.id))
							else:
								pass
					else:
						pass


					for m in i.addpn_grp_association:
						addon_q = Addons.objects.filter(active_status=1,addon_group_id=m,
													addon_group_id__is_crust=0,addon_group__active_status=1)
						for n in addon_q:
							temp_alladdon_without_crust_data = \
							zomatoMenuTempAllAddonData.objects.filter(zomato_addon_grp_id=\
									"AG-"+str(m),zomato_addon_id="A-"+str(n.id))
							if temp_alladdon_without_crust_data.count()==0:
								addon_dict = {}
								addon_dict["ref_id"] = "A-"+str(n.id)
								addon_dict["title"] = n.name
								addon_dict["price"] = n.addon_amount
								# addon_dict["description"] = None
								addon_dict["available"] = True
								addon_dict["sold_at_store"] = True
								addon_dict["food_type"] = 1
								# addon_dict["translations"] = []
								addon_dict["opt_grp_ref_ids"] = []
								addon_dict["opt_grp_ref_ids"].append("AG-"+str(m))
								addon_dict["nested_opt_grps"] = []
								# addon_dict["language"] = []
								sync_data["options"].append(addon_dict)
								temp_alladdon_without_crust_create = \
								zomatoMenuTempAllAddonData.objects.create(zomato_addon_grp_id=\
									"AG-"+str(m),zomato_addon_id="A-"+str(n.id))
							else:
								pass


				product_update = ProductOutletWise.objects.\
				filter(sync_product=i.id,sync_outlet__outlet=outlet_id).\
				update(sync_status="in_progress")
			else:
				pass
	return sync_data