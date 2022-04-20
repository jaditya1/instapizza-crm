import re
import os
from ZapioApi.api_packages import *
from Product.models import FoodType, Product, ProductCategory, ProductsubCategory,\
	AddonDetails,Tag, Variant
from django.db.models import Q
from Outlet.models import OutletProfile
from django.db.models import Max
from Configuration.models import TaxSetting

 # Validation check
def err_check(data):
	err_message = {}
	if type(data["product_image"]) != str:
		im_name_path =  data["product_image"].file.name
		im_size = os.stat(im_name_path).st_size
		if im_size > 500*1024:
			err_message["image_size"] = "Product image can'nt excced the size more than 500kb!!"
	else:
		if data["product_image"] != "":
			pass
		else:
			data["product_image"] = None
	if data["has_variant"] == "true":
		data["has_variant"]= 1
	else:
		data["has_variant"]= 0
	if data["has_variant"] == 0 or data["has_variant"] == 1:
		pass
	else:
		err_message["has_variant"] = "Has variant flag is not set!!"
	if data["has_variant"] == 0:
		data["variant_deatils"] = None
		try:
			data["price"] = float(data["price"])
			data["discount_price"] = float(data["discount_price"])
		except Exception as e:
			err_message["price"] = "Price or Discounted price value is not valid!!"
	else:
		data["price"] = 0
		data["discount_price"] = 0
		varint_unique_list = []
		if len(data["variant_deatils"]) != 0:
			for i in data["variant_deatils"]:
				if "name" in i and  "price" in i and "discount_price" in i and "addon_group" in i and \
					"nested_crust" in i:
					pass
				else:
					err_message["variant_detail"] = \
					"Variant Price, Nested crust and name value are not set!!"
					break	
				if i["name"] not in varint_unique_list:
					varint_unique_list.append(i["name"])
				else:
					err_message["duplicate_variant"] = "Variants are duplicate!!"
					break

				err_message["varinat_name"] = \
				only_required(i["name"],"Variant name")
				# validation_master_anything(i["name"],"Variant name",
				# username_re,3)
				
				if err_message["varinat_name"] != None:
					break
				try:
					i["price"] = float(i["price"])
					i["discount_price"] = float(i["discount_price"])
				except Exception as e:
					err_message["varinat_price"] = \
					"Variant Price value is not valid!!"
					break

				if err_message["varinat_name"] != None:
					break
				else:
					try:
						i["nested_crust"] = int(i["nested_crust"])
					except Exception as e:
						err_message["variant_nested_crust"] = "Nested crust value not set!!"
						break
		else:
			err_message["variant_detail"] = \
					"Variant Price and name value is not set!!"
	if len(data["tags"]) == 0:
		pass
	else:
		for i in data["tags"]:
			err_message["tags"] = \
			validation_master_anything(str(i),"Tag", contact_re,1)
			if err_message["tags"] == None:
				pass
			else:
				break 
	if len(data["tax_association"]) == 0:
		err_message["tax_association"] = "No Taxes are associated!!"
	else:
		for i in data["tax_association"]:
			err_message["tax_association"] = \
			validation_master_anything(str(i),"Tax", contact_re,1)
			if err_message["tax_association"] == None:
				pass
			else:
				break 
	if len(data["included_platform"]) == 0:
		pass
	else:
		for i in data["included_platform"]:
			if i != "swiggy" and i != "zomato":
				err_message["included_platform"] = \
				"Invalid plateform is supplied!!"
				break
			else:
				pass
	err_message["product_name"] = \
			only_required(data["product_name"],"Product")
			# validation_master_anything(data["product_name"],
			# "Product name",product_re, 3)
	err_message["product_desc"] = \
		only_required(data["product_desc"],"Product Desription")
		# validate_anything(data["product_desc"], description_re, 
		# 	zero__re,3, "Product Desription")
	err_message["product_code"] = \
		validate_anything(data["product_code"], username_re, 
			zero__re,3, "Product Code")
	err_message["food_type"] = \
				validation_master_anything(str(data["food_type"]),
				"Food Type",contact_re, 1)
	err_message["product_category"] = \
				validation_master_anything(str(data["product_category"]),
				"Category",contact_re, 1)
	err_message["priority"] = \
				validation_master_anything(data["priority"],
				"Priority",contact_re, 1)
	if data["is_recommended"] != "true" and data["is_recommended"] != "false":
		err_message["is_recommended"] = \
		"Recommended flag is not set!!"
	else:
		pass

	#kot description validation
	kot_desc = data["kot_desc"]
	if "make_table" in kot_desc and "cut_table" in kot_desc:
		make_table = kot_desc["make_table"]
		cut_table = kot_desc["cut_table"]
		if len(make_table) != 0:
			for i in make_table:
				if "description" in i:
					err_message["desc_description"] = \
					only_required(i["desc_description"], "Make Table Product description step")
					if err_message["desc_description"] != None:
						break
					else:
						pass
				else:
					pass

				if "crust" in i:
					if "variant" in i: 
						err_message["crust_description"] = \
						only_required(i["crust_description"], "Make Table Crust step")
						if err_message["crust_description"] != None:
							break
						else:
							pass
					else:
						err_message["crust_variant"] = \
						"Variant key is not provided!!"
				else:
					pass
														

				if "base_sauce" in i:
					err_message["base_sauce_description"] = \
					only_required(i["base_sauce_description"], "Make Table Base Sauce step")
					if err_message["base_sauce_description"] != None:
						break
					else:
						pass
				else:
					pass

				if "toppings" in i:
					err_message["toppings_description"] = \
					only_required(i["toppings_description"], "Make Table toppings step")
					if err_message["toppings_description"] != None:
						break
					else:
						pass
				else:
					pass

				if "cheese" in i:
					err_message["cheese_description"] = \
					only_required(i["cheese_description"], "Make Table cheese step")
					if err_message["cheese_description"] != None:
						break
					else:
						pass
				else:
					pass
		else:
			pass

		if len(cut_table) != 0:
			for j in cut_table:
				if "sauces_on_top" in j:
					err_message["sauces_on_top_description"] = \
					only_required(j["sauces_on_top_description"], "Cut Table sauces on top step")
					if err_message["sauces_on_top_description"] != None:
						break
					else:
						pass
				else:
					pass

				if "garnishes" in j:
					err_message["garnishes_description"] = \
					only_required(j["garnishes_description"], "Cut Table garnishing step")
					if err_message["garnishes_description"] != None:
						break
					else:
						pass
				else:
					pass

				if "fried_filling" in j:
					err_message["fried_filling"] = \
					only_required(j["fried_filling"], "Cut Table fried filling step")
					if err_message["fried_filling"] != None:
						break
					else:
						pass
				else:
					pass

				if "seasoning" in j:
					err_message["seasoning"] = \
					only_required(j["seasoning"], "Cut Table seasoning step")
					if err_message["seasoning"] != None:
						break
					else:
						pass
				else:
					pass

				if "add_on" in j:
					err_message["add_on"] = \
					only_required(j["add_on"], "Cut Table garnishing step")
					if err_message["add_on"] != None:
						break
					else:
						pass
				else:
					pass
		else:
			pass
	else:
		pass
	if any(err_message.values())==True:
		err = {
			"success"	: 	False,
			"error" 	: 	err_message,
			"message" 	: 	"Please correct listed errors!!"
			}
		return err
	else:
		return None


def unique_record_check(data, Company_id):
	err_message = {}
	if data["is_recommended"] == "true":
		data["is_recommended"]= 1
	else:
		data["is_recommended"]= 0
	if "id" in data:
		unique_check = Product.objects.filter(~Q(id=data["id"]),\
			Q(product_name__iexact=data["product_name"]),\
			Q(product_category=data["product_category"]))
	else:
		unique_check = Product.objects.filter(Q(product_name__iexact=data["product_name"]),\
								Q(product_category=data["product_category"]))
	if unique_check.count() != 0:
		err_message["unique_check"] = "Product with this name already exists!!"
	else:
		pass
	if "id" in data:
		unique_code_check = Product.objects.filter(~Q(id=data["id"]),\
			Q(product_code__iexact=data['product_code']),\
			Q(product_category=data["product_category"]))\
			.exclude(product_code__isnull=True).exclude(product_code__exact='')
	else:
		unique_code_check = Product.objects.filter(Q(product_code__iexact=data['product_code']),\
							Q(product_category=data["product_category"]))\
							.exclude(product_code__isnull=True).exclude(product_code__exact='')
	if unique_code_check.count() != 0:
		err_message["unique_code_check"] = "Product with this code already exists!!"
	else:
		pass
	# if "id" in data:
	# 	priority_check = Product.objects.filter(~Q(id=data["id"]),\
	# 					Q(priority=int(data["priority"])))
	# else:
	# 	priority_check = Product.objects.filter(Q(priority=int(data["priority"])))
	# if priority_check.count() != 0:
	# 	max_priority = \
	# 	Product.objects.aggregate(Max('priority'))
	# 	suggestion = max_priority["priority__max"] + 1
	# 	err_message["priority_check"] = \
	# 	"This priority is already assigned to other product..You can try "+str(suggestion)+" as priority!!"
	# else:
	# 	pass
	Addon_check = AddonDetails.objects.filter(active_status=1)
	if len(data["addpn_grp_association"]) != 0:
		for q in data['addpn_grp_association']:
			add_check = Addon_check.filter(id=q)
			if add_check.count() == 1:
				pass
			else:
				err_message["addpn_grp_association"] = \
				"Addon Group Association is not valid..Please check!!"
	else:
		pass
	tag_check = Tag.objects.filter(active_status=1)
	if len(data["tags"]) != 0:
		for q in data['tags']:
			add_check = tag_check.filter(id=q)
			if add_check.count() == 1:
				pass
			else:
				err_message["tags"] = \
				"Tag is not valid..Please check!!"
	else:
		pass
	tax_check = TaxSetting.objects.filter(active_status=1)
	if tax_check.count() == 0:
		err_message["tax_association"] = \
			"Tax is not configured at super-admin level!!"
	else:
		pass
	for q in data["tax_association"]:
		check = tax_check.filter(id=q)
		if check.count() == 1:
			pass
		else:
			err_message["tax_association"] = \
			"Tax is not valid!!"
			break
	if data["variant_deatils"] == None:
		pass
	else:
		for i in data["variant_deatils"]:			
			v_check = Variant.objects.filter(variant=i["name"],Company=Company_id, active_status=1)
			if v_check.count()==0:
				err_message["variant_deatils"] = "Variant is not valid or active!!"
				break
			else:
				pass
	if any(err_message.values())==True:
		err = {
			"success": False,
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			}
		return err
	else:
		return None