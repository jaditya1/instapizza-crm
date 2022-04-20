from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
from django.db.models import Q
from django.db.models import Max

#Serializer for api
from rest_framework import serializers
from Product.models import ProductCategory, AddonDetails, Variant,Addons
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from rest_framework_tracking.mixins import LoggingMixin

class AddonDetailsSerializer(serializers.ModelSerializer):
	class Meta:
		model = AddonDetails
		fields = '__all__'

class AddonSerializer(serializers.ModelSerializer):
	class Meta:
		model = Addons
		fields = '__all__'

class AddonCreationUpdation(LoggingMixin,APIView):
	"""
	Addon Details Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update addon details within brand.

		Data Post: {
			"id"                   	: 	"1",(Send this key in update record case,else it is not required!!)
			"addon_gr_name"		   	: 	"Pizza",
			"min_addons"		   	: 	"1",
			"priority"             	: 	"1",
			"max_addons" 	       	: 	"1",
			"description"          	: 	"eee",
			"product_variant"      	: 	"1",(optional key)
			"addon_grp_type"		:	"0",
			"is_zomato_crust"		:	True,
			"zomato_nested_crusts"	:	["1","2","3"]
		}

		Response: {

			"success": True, 
			"message": "Addon details creation/updation api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			from Brands.models import Company
			data = request.data
			data["company_auth_id"] = request.user.id
			user = request.user.id
			cid = get_user(user)
			data['Company'] = cid
			err_message = {}
			if data["is_zomato_crust"] != True and data["is_zomato_crust"] != False:
				err_message["is_zomato_crust"] = "Zomato crust flag value is not set!!"
			else:
				pass
			err_message["addon_gr_name"] = \
					validation_master_anything(data["addon_gr_name"],
					"Addon Group Name",username_re, 3)
			if data["priority"] != None:
				err_message["priority"] = \
					validation_master_anything(str(data["priority"]),
					"Priority",contact_re, 1)
			else:
				pass

			err_message["addon_grp_type"] = None
			if data["addon_grp_type"]!="0" and data["addon_grp_type"]!="1" and data["addon_grp_type"]!="2"\
				and data["addon_grp_type"]!="3" and data["addon_grp_type"]!="4":
				err_message["addon_grp_type"] = "Please Select valid addon group type!!"
			else:
				pass
			if len(data["zomato_nested_crusts"])!=0:
				for i in data["zomato_nested_crusts"]:
					record_addon_grp = \
					AddonDetails.objects.filter(Q(id=i),Q(active_status=1))
					if record_addon_grp.count()==0:
						err_message["zomato_nested_crusts"] = "Zomato Nested Crusts are not valid!!"
						break
					else:
						err_message["zomato_nested_crusts"] = None
			else:
				err_message["zomato_nested_crusts"] = None
				data["zomato_nested_crusts"] = None
			err_message["description"] = \
					validation_master_anything(data["description"],
					"Description",description_re, 3)
			try:
				data["min_addons"] = int(data["min_addons"])
				err_message["min_addons"] = None
			except Exception as e:
				err_message["min_addons"] = "Minimum addons value is not valid!!"
			try:
				data["max_addons"] = int(data["max_addons"])
				err_message["max_addons"] = None
			except Exception as e:
				err_message["max_addons"] = \
				"Maximum addons value is not valid!!"
			if err_message["min_addons"] == None and err_message["max_addons"] == None:
				if int(data["max_addons"]) <  int(data["min_addons"]):
					err_message["min_max"] = "Minimum & Maximum Addons are not properly provided!!"
			else:
				pass
			if data["product_variant"] != "":
				unique_check = AddonDetails.objects.\
				filter(addon_gr_name__iexact=data["addon_gr_name"],
												product_variant=data["product_variant"])
			else:
				unique_check = AddonDetails.objects.\
				filter(addon_gr_name__iexact=data["addon_gr_name"])
			if unique_check.count() != 0 and "id" not in data:
				err_message["unique_check"] = "Addon group with this name already exists!!"
			else:
				pass
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			if int(data["max_addons"]) > 100:
				err_message = {}
				err_message["max_addons"] = \
				"Maximum addons can'nt be more than 100!!"
				if any(err_message.values())==True:
					return Response({
						"success": False,
						"error" : err_message,
						"message" : "Please correct listed errors!!"
						})
			if data["product_variant"] != "":
				Variant_query = Variant.objects.filter(id=data["product_variant"])
				if Variant_query.count() != 0:
					pass
				else:
					return Response(
						{
							"success": False,
		 					"message": "Variant Id is not valid!!"
						}
						)
			else:
				pass
			data["Company"] = cid
			if "id" in data:
				addons_record = AddonDetails.objects.filter(id=data['id'])
				if addons_record.count() == 0:
					return Response(
					{
						"success": False,
	 					"message": "Addon data is not valid to update!!"
					}
					)
				else:
					data["updated_at"] = datetime.now()
					if data["product_variant"] != "":
						unique_check = \
						AddonDetails.objects.filter(~Q(id=data["id"]),\
										Q(addon_gr_name__iexact=data['addon_gr_name']),\
										Q(product_variant=data["product_variant"]),\
										Q(Company=data["Company"]))
					else:
						unique_check = \
						AddonDetails.objects.filter(~Q(id=data["id"]),\
										Q(addon_gr_name__iexact=data['addon_gr_name']),\
										Q(product_variant=None),Q(Company=data["Company"]))
					if unique_check.count() == 0:
						addon_serializer = \
						AddonDetailsSerializer(addons_record[0],data=data,partial=True)
						if addon_serializer.is_valid():
							data_info = addon_serializer.save()
							info_msg = "Addon group is updated successfully!!"
						else:
							return Response({
								"success": False, 
								"message": str(addon_serializer.errors),
								})
					else:
						err_message = {}
						err_message["unique_check"] = "Addon group with this name already exists!!"
						return Response({
									"success": False,
									"error" : err_message,
									"message" : "Please correct listed errors!!"
									})
			else:
				addon_serializer = AddonDetailsSerializer(data=data)
				if addon_serializer.is_valid():
					data_info = addon_serializer.save()
					info_msg = "Addon group is created successfully!!"
				else:
					return Response({
						"success": False, 
						"message": str(addon_serializer.errors),
						})
			return Response({
						"success": True, 
						"message": info_msg
						})
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class AddonAssociateCreationUpdation(LoggingMixin,APIView):
	"""
	Addon Details Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update addon details within brand.

		Data Post: {
			"id"                   : "1",
			"associated_addons"    : [
				{
									"addon_name" 	: 	"Vegeterain Topping",
									"price"      	: 	"45"
									"priority"      : 	"1"
			},
			{
									"addon_name" 	: 	"Shudh Shakahari",
									"price"      	: 	"25"
									"priority"      : 	"2"
			}]
		}

		Response: {

			"success"	: 	True, 
			"message"	: 	"Addon group Association creation/updation api worked well!!",
			"data"		: 	final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			mutable = request.POST._mutable
			addon_data = {}
			request.POST._mutable = True
			data = request.data
			err_message = {}
			user = request.user.id
			cid = get_user(user)
			data['Company'] = cid
			alld = AddonDetails.objects.filter(id=data['id'],Company=cid, active_status=1)
			if alld.count() == 0:
				return Response({
					"success": False,
					"message" : "Addon Group is not valid!!"		
					})
			addon_record = Addons.objects.filter(addon_group=data["id"])
			if addon_record.count() > 0:
				addon_record.update(active_status=0)
			else:
				pass
			if len(data["associated_addons"]) != 0:
				for i in data['associated_addons']:
					if "addon_name" in i and "price" in i:
						pass
					else:
						err_message["addon_detail"] = \
					"addon name, price is not set!!"
						break
					try:
						i["price"] = float(i["price"])
					except Exception as e:
						err_message["price"] = "Price is not valid!!"
						break
					try:
						i["price"] = int(i["price"])
					except Exception as e:
						err_message["price"] = "Priority is not valid!!"
						break
					err_message["addon_name"] = \
								only_required(i["addon_name"], "Addon name")
								# validation_master_anything(i["addon_name"],"Addon name",
								# username_re,3)
					if err_message["addon_name"] != None:
						break
					else:
						pass
					addon_data['name']          = i['addon_name']
					addon_data['addon_amount']  = i['price']
					addon_data['addon_group']  = data['id']
					addon_data['Company']  = cid
					addon_data['active_status'] = True
					addon_data['priority'] = i['priority']
					addon_record_filter = addon_record.filter(name=i['addon_name'])
					if addon_record_filter.count() == 0:
						addon_serializer = AddonSerializer(data=addon_data)
						if addon_serializer.is_valid():
							data_info = addon_serializer.save()
						else:
							return Response({
								"success": False, 
								"message": str(addon_serializer.errors),
								})
					else:
						update_serializer = \
						AddonSerializer(addon_record_filter[0],data=addon_data,partial=True)
						if update_serializer.is_valid():
							data_info = update_serializer.save()
						else:
							return Response({
								"success": False, 
								"message": str(update_serializer.errors),
								})
			else:
				err_message["addon_detail"] = \
					"addon name, price is not set!!"
			if any(err_message.values())==True:
				return Response({
								"success": False,
								"error" : err_message,
								"message" : "Please correct listed errors!!"
							})
			addon_grp = {}
			addon_grp["associated_addons"] = data["associated_addons"]
			addon_serializer = \
			AddonDetailsSerializer(alld[0],data=addon_grp,partial=True)
			if addon_serializer.is_valid():
				data_info = addon_serializer.save()
				info_msg = "Addon group is updated successfully!!"
			else:
				return Response({
					"success": False, 
					"message": str(addon_serializer.errors),
					})
			return Response({
						"success": True, 
						"message": "Addon group Association creation/updation api worked well!!",
						})
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
