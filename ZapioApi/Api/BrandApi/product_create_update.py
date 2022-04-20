from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
import json
from datetime import datetime
import os
from django.db.models import Max
from ZapioApi.Api.BrandApi.listing.listing import ProductlistingSerializer
from ZapioApi.Api.BrandApi.Validation.product_error_check import *
from Brands.models import Company

#Serializer for api
from rest_framework import serializers
from Product.models import FoodType, Product, ProductCategory, ProductsubCategory,\
	AddonDetails, Variant, ProductApiLog, KotSteps
from urbanpiper.models import ProductSync
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

from ZapioApi.Api.BrandApi.outletmgmt.availability.available import availability_sync
from _thread import start_new_thread


def kot_data_process(kot_desc, company_id, product_id):
	record_delete = KotSteps.objects.filter(product_id=product_id).delete()
	if "make_table" in kot_desc and "cut_table" in kot_desc:
		make_table = kot_desc["make_table"]
		cut_table = kot_desc["cut_table"]
		if len(make_table) != 0:
			for i in make_table:
				if "description" in i:
					record_create = \
					KotSteps.objects.create(Company_id=company_id,product_id=product_id,
							kot_category='0', step_name='0',kot_desc=i["desc_description"])
				else:
					pass

				if "crust" in i:
					if i["variant"] == None:
						v_id = None
					else:
						v_id = i["variant"]
					record_base_sauce_create = \
					KotSteps.objects.create(Company_id=company_id,product_id=product_id,
							kot_category='0', step_name='1',kot_desc=i["crust_description"], variant_id=v_id)
				else:
					pass

				if "base_sauce" in i:
					record_base_sauce_create = \
					KotSteps.objects.create(Company_id=company_id,product_id=product_id,
							kot_category='0', step_name='2',kot_desc=i["base_sauce_description"])
				else:
					pass


				if "toppings" in i:
					record_toppings_create = \
					KotSteps.objects.create(Company_id=company_id,product_id=product_id,
							kot_category='0', step_name='3',kot_desc=i["toppings_description"])
				else:
					pass


				if "cheese" in i:
					record_cheese_create = \
					KotSteps.objects.create(Company_id=company_id,product_id=product_id,
							kot_category='0', step_name='5',kot_desc=i["cheese_description"])
					
				else:
					pass
		else:
			pass


		if len(cut_table) != 0:
			for j in cut_table:
				if "sauces_on_top" in j:
					record_sauces_on_top_create = \
					KotSteps.objects.create(Company_id=company_id,product_id=product_id,
							kot_category='1', step_name='7',kot_desc=j["sauces_on_top_description"])
				else:
					pass

				if "garnishes" in j:
					record_garnishes_create = \
					KotSteps.objects.create(Company_id=company_id,product_id=product_id,
							kot_category='1', step_name='8',kot_desc=j["garnishes_description"])
				else:
					pass

				if "fried_filling" in j:
					record_fied_update = \
					KotSteps.objects.create(Company_id=company_id,product_id=product_id,
							kot_category='1', step_name='10',kot_desc=j["fried_filling"])
				else:
					pass

				if "seasoning" in j:
					record_seasoning_update = \
					KotSteps.objects.create(Company_id=company_id,product_id=product_id,
							kot_category='1', step_name='11',kot_desc=j["seasoning"])
				else:
					pass

				if "add_on" in j:
					record_seasoning_update = \
					KotSteps.objects.create(Company_id=company_id,product_id=product_id,
							kot_category='1', step_name='9',kot_desc=j["add_on"])
				else:
					pass



		else:
			pass
	else:
		pass
	return "kot_data_process_done"


def ApiTrack(request_data):
	file_data = None
	if "product_image" in request_data:
		if type(request_data["product_image"]) != str:
			file_data = request_data["product_image"]
		del request_data["product_image"]
	else:
		pass
	record_create = ProductApiLog.objects.create(request_data=request_data,request_file=file_data)
	record_id = record_create.id
	return record_id




class ProductCreationUpdation(APIView):
	"""
	Product Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update products.

		Data Post: {
					   "id":661,
					   "product_category":"64",
					   "product_subcategory":"",
					   "product_name":"Cheese Burstjggjh",
					   "food_type":"8",
					   "priority":"1",
					   "product_code":"",
					   "product_desc":"",
					   "product_image":"",
					   "has_variant":"true",
					   "price":"",
					   "discount_price":"",
					   "variant_deatils":[
					      {
					         "name":"Large",
					         "price":"245",
					         "discount_price":"209",
					         "addon_group":[
					            166
					         ],
					         "nested_crust" : "4"
					      }
					   ],
					   "addpn_grp_association":[
					      
					   ],
					   "tax_association":[
					      1,
					      2
					   ],
					   "tags":[
					      
					   ],
					   "is_recommended":"true",
					   "included_platform":[
					      "swiggy",
					      "zomato"
					   ],
					   "kot_desc":{
					      "make_table":[
					         {
					            "description":"0",
					            "desc_description":"sdcscdcdscscscs, dfvvdf"
					         },
					         {
					            "crust":"1",
					            "variant" : "23",
					            "crust_description":"sdcsdccdwcc, dfvdfv, fvdv"
					         },
					         {
					            "crust":"1",
					            "variant" : "24",
					            "crust_description":"sdcsdccdwcc, dfvdfv, fvdv"
					         },
					         {
					            "crust":"1",
					            "variant" : "25",
					            "crust_description":"sdcsdccdwcc, dfvdfv, fvdv"
					         },
					         {
					            "base_sauce":"2",
					            "base_sauce_description":"sdcsdccdwcc, dfvdfv, fvdv"
					         },
					         {
					            "toppings":"4",
					            "toppings_description":"dfdfvdvdvdvdvdv, effvdf, dfvv, dfvdfvd"
					         },
					         {
					            "cheese":"6",
					            "cheese_description":"dcdsc, sdcsdc, yyuyuy"
					         }
					      ],
					      "cut_table":[
					         {
					            "sauces_on_top":"8",
					            "sauces_on_top_description":"sdcscdcdscscscs, dfvvdf"
					         },
					         {
					            "garnishes":"9",
					            "garnishes_description":"sdcsdccdwcc, dfvdfv, fvdv"
					         }
					      ]
					   }
					}

		Response: {

			"success": True, 
			"message": "Product creation/updation api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			success = True
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			# request_data = data.copy()
			# apitrack_id = ApiTrack(request_data)
			# apitrack_record =  ProductApiLog.objects.filter(id=apitrack_id)
			# data2 = json.loads(data["addpn_grp_association"])
			# data3 = json.loads(data["variant_deatils"])
			# data4 = json.loads(data["tags"])
			# data5 = json.loads(data["tax_association"])
			# data6 = json.loads(data["included_platform"])
			# data7 = json.loads(data["kot_desc"])
			# data["addpn_grp_association"] = data2
			# data["variant_deatils"] = data3
			# data["tags"] = data4
			# data["tax_association"] = data5
			# data["included_platform"] = data6
			# data["kot_desc"] = data7
			auth_id = request.user.id
			Company_id = get_user(auth_id)
			validation_check = err_check(data)
			unique_check = None
			if validation_check != None:
				success = False
			else:
				unique_check = unique_record_check(data, Company_id)
			if unique_check != None:
				success = False
			if success == True:
				cat_query = ProductCategory.objects.filter(id=data["product_category"])
				if cat_query.count() != 0:
					pass
				else:
					success = False
					msg = "Category is not valid!!"
				if data["product_subcategory"] != "":
					sucat_query = ProductsubCategory.objects.filter(id=data["product_subcategory"])
					if sucat_query.count() != 0:
						pass
					else:
						success = False
						msg = "Sub-Category id is not valid to update!!"
				else:
					pass
				food_query = FoodType.objects.filter(id=data["food_type"])
				if food_query.count() != 0:
					pass
				else:
					success = False
					msg = "FoodType id is not valid to update!!"
			else:
				pass

			if success == True:
				data["active_status"] = 1
				if "id" in data:
					record = Product.objects.filter(id=data['id'])
					if record.count() == 0:
						success = False
						msg = "Product data is not valid to update!!"
					else:
						if success == True:
							data["updated_at"] = datetime.now()
							update_data = \
							record.update(product_category_id=data["product_category"],\
							product_subcategory_id=data["product_subcategory"],product_name=data["product_name"],\
							food_type_id=data["food_type"],priority=data["priority"],product_code=data["product_code"],\
							product_desc=data["product_desc"],has_variant=data["has_variant"],price=data["price"],\
							variant_deatils=data["variant_deatils"],addpn_grp_association=data["addpn_grp_association"],\
							active_status=data["active_status"],\
							updated_at=datetime.now(),discount_price=data["discount_price"],
							Company_id=Company_id,tags=data["tags"],
							is_recommended=data["is_recommended"],tax_association=data["tax_association"],
							included_platform = data["included_platform"])
							if data["product_image"] != None and data["product_image"] != "":
								product = Product.objects.get(id=data["id"])
								product.product_image = data["product_image"]
								product.save()
							else:
								pass
							if update_data:
								p_id = data["id"]
								msg = "Product is updated successfully!!"
							else:
								success = False
								msg = str(serializer.errors)
						else:
							pass
				else:
					p_query = \
						Product.objects.create(product_category_id=data["product_category"],\
						product_subcategory_id=data["product_subcategory"],product_name=data["product_name"],\
						food_type_id=data["food_type"],priority=data["priority"],product_code=data["product_code"],\
						product_desc=data["product_desc"],product_image=data["product_image"],\
						has_variant=data["has_variant"],price=data["price"],variant_deatils=data["variant_deatils"],\
						addpn_grp_association=data["addpn_grp_association"],\
						active_status=data["active_status"],created_at=datetime.now(),\
						discount_price=data["discount_price"],Company_id=Company_id,tags=data["tags"],\
						tax_association=data["tax_association"],is_recommended=data["is_recommended"],
						included_platform=data["included_platform"])
					if p_query:
						data_info=p_query
						p_id = data_info.id
						msg = "Product is created successfully!!"
					else:
						success = False
						msg = str(serializer.errors)
						
				#sync product logic starts from here
				if data["variant_deatils"]!=None and len(data["variant_deatils"]) != 0:
					for i in data["variant_deatils"]:
						v_rec = Variant.objects.filter(variant=i["name"],Company=Company_id)
						q = v_rec[0]
						sync_check = ProductSync.objects.filter(product=p_id,variant=q.id,\
									category=data["product_category"], company=Company_id)
						if sync_check.count() == 0:
							sync_create = ProductSync.objects.create(product_id=p_id,variant_id=q.id,\
									category_id=data["product_category"], price=i["price"],\
									discount_price=i["discount_price"],company_id=Company_id,\
									addpn_grp_association=i["addon_group"],\
									zomato_crust_id_id=i["nested_crust"])
						else:
							sync_update = sync_check.update(price=i["price"],\
									discount_price=i["discount_price"],\
									addpn_grp_association=i["addon_group"],active_status=0,
									zomato_crust_id_id=i["nested_crust"])
				else:
					sync_check = ProductSync.objects.filter(product=p_id,
									category=data["product_category"], company=Company_id, variant=None)
					if sync_check.count() == 0:
						sync_create = ProductSync.objects.create(product_id=p_id,\
								category_id=data["product_category"], price=data["price"],\
								discount_price=data["discount_price"],company_id=Company_id,\
								addpn_grp_association=data["addpn_grp_association"])
					else:
						sync_update = sync_check.update(price=data["price"],\
								discount_price=data["discount_price"],\
								addpn_grp_association=data["addpn_grp_association"],active_status=0)
				#sync product logic ends here
			else:
				pass
			if validation_check != None:
				# apitrack_record.update(response_data=validation_check)
				return Response(validation_check)
			if unique_check != None:
				# apitrack_record.update(response_data=unique_check)
				return Response(unique_check)

			kot_process = kot_data_process(data["kot_desc"], Company_id, p_id)
			valid_response = {}
			valid_response["success"] = success
			valid_response["message"] = msg
			# apitrack_record.update(response_data=valid_response)
			start_new_thread(availability_sync, (data["product_category"],Company_id))
			return Response(valid_response)

		except Exception as e:
			exception_response = {}
			exception_response["success"] = False
			exception_response["message"] = "Error happened!!"
			exception_response["errors"] = str(e)
			# apitrack_record.update(response_data=exception_response)
			return Response(exception_response)
