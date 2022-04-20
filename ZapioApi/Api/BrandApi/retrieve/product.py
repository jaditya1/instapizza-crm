from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
from zapio.settings import Media_Path
#Serializer for api
from rest_framework import serializers
from Product.models import Product, AddonDetails, Tag,Variant, KotSteps
from urbanpiper.models import *
from django.db.models import Q
from Configuration.models import TaxSetting

class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = '__all__'


class ProductRetrieval(APIView):
	"""
	Product retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Product data.

		Data Post: {
			"id"                   : "60"
		}

		Response: {

			"success": True, 
			"message": "Product retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Product Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = Product.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided Product data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["product_category"] = record[0].product_category_id
				q_dict["product_subcategory"] = record[0].product_subcategory_id
				q_dict["cat_detail"] = []
				cat_dict = {}
				cat_dict["label"] = record[0].product_category.category_name
				cat_dict["key"] = record[0].product_category_id
				cat_dict["value"] = record[0].product_category_id
				q_dict["cat_detail"].append(cat_dict)
				if q_dict["product_subcategory"] != None:
					q_dict["product_subcategory_name"] = record[0].product_subcategory.subcategory_name
					q_dict["subcat_detail"] = []
					subcat_dict = {}
					subcat_dict["label"] = record[0].product_subcategory.subcategory_name
					subcat_dict["key"] = record[0].product_subcategory_id
					subcat_dict["value"] = record[0].product_subcategory_id
					q_dict["subcat_detail"].append(subcat_dict)
				else:
					q_dict["product_subcategory_name"] = None 
				q_dict["product_name"] = record[0].product_name
				q_dict["food_type"] = record[0].food_type.food_type
				q_dict["foodtype_detail"] = []
				food_dict = {}
				food_dict["label"] = record[0].food_type.food_type
				food_dict["key"] = record[0].food_type_id
				food_dict["value"] = record[0].food_type_id
				q_dict["foodtype_detail"].append(food_dict)
				q_dict["priority"] = record[0].priority
				q_dict["product_image"] = record[0].product_image
				full_path = Media_Path
				if q_dict["product_image"] != None and q_dict["product_image"]!="":
					q_dict["product_image"] = full_path+str(q_dict["product_image"])
				else:
					q_dict["product_image"] = None
				q_dict["product_code"] = record[0].product_code
				q_dict["product_desc"] = record[0].product_desc
				# q_dict["kot_desc"] = record[0].kot_desc
				q_dict["has_variant"] = record[0].has_variant
				q_dict["price"] = record[0].price
				q_dict["is_recommended"] = record[0].is_recommended
				q_dict["discount_price"] = record[0].discount_price
				q_dict["variant_deatils"] = record[0].variant_deatils
				q_dict["is_recommended"] = record[0].is_recommended
				va = q_dict["variant_deatils"] 
				if va != None:
					for v in va:
						if "name" in v:
							v_name = v["name"]
							v["name"] = {}
							v["name"]["id"] = v_name
							p_id= record[0].id
							v["name"]["label"] = v_name
							v["name"]["key"] = v_name
							v["dis"] = v["discount_price"]
							v_id = Variant.objects.filter(variant=v_name)[0].id
							p_v=ProductSync.objects.filter(Q(product_id=p_id),\
								  Q(variant_id=v_id))
							if p_v.count() > 0:
								v['u_id'] = p_v[0].id
							else:
								pass
							v_addon = v["addon_group"]
							v["addonGroup"] = []
							if len(v_addon) != 0:
								for i in v_addon:
									v_addon_dict = {}
									addon_q = AddonDetails.objects.filter(id=i)
									if addon_q.count() > 0:
										v_addon_dict["value"] = addon_q[0].id
										v_addon_dict["key"] = addon_q[0].id
										v_addon_dict["label"] = addon_q[0].addon_gr_name
										v["addonGroup"].append(v_addon_dict)
									else:
										pass
							else:
								pass
							if "nested_crust" in v:
								nested_crust = v["nested_crust"]
								nested_q = AddonDetails.objects.filter(id=nested_crust)[0]
								# v["nestedCrust"] = []
								# nested_dict = {}
								# nested_dict["value"] = nested_q.id
								# nested_dict["key"] = nested_q.id
								# nested_dict["label"] = nested_q.addon_gr_name
								# v["nestedCrust"].append(nested_dict)

								v["nestedCrust"] = {}
								v["nestedCrust"]["value"] = nested_q.id
								v["nestedCrust"]["key"] = nested_q.id
								if nested_q.description == None:
									v["nestedCrust"]["label"] = nested_q.addon_gr_name
								else:
									v["nestedCrust"]["label"] = nested_q.addon_gr_name+"("+\
														nested_q.description+")"
								del v["nested_crust"]
								v["nested_crust"] = v.pop("nestedCrust")
							else:
								pass
							del v["addon_group"]
							del v["discount_price"]
						else:
							pass
					q_dict["variant_deatils"] = va
				else:
					pass
				addons_detail = record[0].addpn_grp_association
				q_dict["addon_details"] = []
				if addons_detail != None:
					for q in addons_detail:
						addon_q = AddonDetails.objects.filter(id=q)
						if addon_q.count() > 0:
							addon_dict = {}
							addon_dict["value"] = addon_q[0].id
							addon_dict["key"] = addon_q[0].id
							addon_dict["label"] = addon_q[0].addon_gr_name
							addon_dict["associated_addons"] = addon_q[0].associated_addons
							q_dict["addon_details"].append(addon_dict)
						else:
							pass
				else:
					pass
				tag_detail  = record[0].tags

				q_dict["tags"] = []
				if tag_detail != None:
					for i in tag_detail:
						tag_q = Tag.objects.filter(id=i)
						if tag_q.count() > 0:
							tag_dict = {}
							tag_dict["value"] = tag_q[0].id
							tag_dict["key"] = tag_q[0].id
							tag_dict["label"] = tag_q[0].tag_name
							q_dict["tags"].append(tag_dict)
						else:
							pass
				else:
					pass
				platform_detail  = record[0].included_platform
				q_dict["platform_detail"] = []
				if platform_detail != None:
					for i in platform_detail:
						tag_dict = {}
						tag_dict["value"] = i
						tag_dict["key"] = i
						tag_dict["label"] = i
						q_dict["platform_detail"].append(tag_dict)
				else:
					pass
				final_result.append(q_dict)
				tax_detail = record[0].tax_association
				q_dict["tax_association"] = []
				if tax_detail != None:
					for i in tax_detail:
						tax_q = TaxSetting.objects.filter(id=i)
						if tax_q.count() != 0:
							tax_dict = {}
							tax_dict["value"] = tax_q[0].id
							tax_dict["key"] = tax_q[0].id
							tax_dict["label"] = str(tax_q[0].tax_name)+" | "+str(tax_q[0].tax_percent)+"%" 
							q_dict["tax_association"].append(tax_dict)
						else:
							pass
				else:
					pass
				kot_record = KotSteps.objects.filter(product_id=data["id"])
				desc_description_record = kot_record.filter(step_name="0",kot_category="0")
				if desc_description_record.count()!=0:
					q_dict["desc_description"] = desc_description_record[0].kot_desc
				else:
					q_dict["desc_description"] = ""

				crust_description_record = kot_record.filter(step_name="1",kot_category="0")
				q_dict["crusts"] = []
				for k in crust_description_record:
					crust_dict = {}
					crust_dict["crust"] = "1"
					if k.variant != None:
						crust_dict["variant"] = k.variant_id
						crust_dict["variant_name"] = k.variant.variant
					else:
						crust_dict["variant"] = None
						crust_dict["variant_name"] = None
					crust_dict["crust_description"] = k.kot_desc
					q_dict["crusts"].append(crust_dict)
				

				base_sauce_description_record = kot_record.filter(step_name="2",kot_category="0")
				if base_sauce_description_record.count()!=0:
					q_dict["base_sauce_description"] = base_sauce_description_record[0].kot_desc
				else:
					q_dict["base_sauce_description"] = ""

				toppings_description_record = kot_record.filter(step_name="3",kot_category="0")
				if toppings_description_record.count()!=0:
					q_dict["toppings_description"] = toppings_description_record[0].kot_desc
				else:
					q_dict["toppings_description"] = ""

				cheese_description_record = kot_record.filter(step_name="5",kot_category="0")
				if cheese_description_record.count()!=0:
					q_dict["cheese_description"] = cheese_description_record[0].kot_desc
				else:
					q_dict["cheese_description"] = ""

				sauces_on_top_description_record = kot_record.filter(step_name="7",kot_category="1")
				if sauces_on_top_description_record.count()!=0:
					q_dict["sauces_on_top_description"] = sauces_on_top_description_record[0].kot_desc
				else:
					q_dict["sauces_on_top_description"] = ""

				fried_description_record = kot_record.filter(step_name="10",kot_category="1")
				if fried_description_record.count()!=0:
					q_dict["fried_filling"] = fried_description_record[0].kot_desc
				else:
					q_dict["fried_filling"] = ""

				seasoning_record = kot_record.filter(step_name="11",kot_category="1")
				if seasoning_record.count()!=0:
					q_dict["seasoning"] = seasoning_record[0].kot_desc
				else:
					q_dict["seasoning"] = ""


				garnishes_description_record = kot_record.filter(step_name="8",kot_category="1")
				if garnishes_description_record.count()!=0:
					q_dict["garnishes_description"] = garnishes_description_record[0].kot_desc
				else:
					q_dict["garnishes_description"] = ""

				addon_record = kot_record.filter(step_name="9",kot_category="1")
				if addon_record.count()!=0:
					q_dict["add_on"] = addon_record[0].kot_desc
				else:
					q_dict["add_on"] = ""
			if final_result:
				return Response({
							"success": True, 
							"message": "Product retrieval api worked well!!",
							"data": final_result,
							})
			else:
				return Response({
							"success": True, 
							"message": "No product data found!!"
							})
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


