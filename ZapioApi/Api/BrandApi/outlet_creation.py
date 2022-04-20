from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.Api.BrandApi.Validation.outlet_error_check import *
from _thread import start_new_thread
from django.db.models import Avg, Max, Min, Sum
from django.db.models import Q
#Serializer for api
from rest_framework import serializers
from Outlet.models import OutletProfile
from Product.models import Product, Product_availability, Category_availability, ProductCategory
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from rest_framework_tracking.mixins import LoggingMixin

def map_products_to_outlet(outlet_id, auth_id):
	product = Product.objects.filter(active_status=1,product_category__Company__auth_user=auth_id)
	category = ProductCategory.objects.filter(active_status=1,Company__auth_user=auth_id)
	now = datetime.now()
	available_category = []
	for i in category:
		available_category.append(i.id)
	cat_availability = Category_availability.objects.filter(outlet_id=outlet_id)
	if cat_availability.count() == 0:
		availability_create = Category_availability.objects.\
		create(outlet_id=outlet_id,available_cat=available_category,created_at=now)
	else:
		pass
	available_product = []
	for i in product:
		available_product.append(i.id)
	outlet_availability = Product_availability.objects.filter(outlet_id=outlet_id)
	if outlet_availability.count() == 0:
		availability_create = Product_availability.objects.\
		create(outlet_id=outlet_id,available_product=available_product,created_at=now)
	else:
		pass
	return "Products & Categories are Mapped!!"

class OutletSerializer(serializers.ModelSerializer):
	class Meta:
		model = OutletProfile
		fields = '__all__'

class OutletCreation(LoggingMixin,APIView):
	"""
	Outlet Creation and update(using id) POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create and  update new outlets within brand.

        create outlets

		Data Post: {
			
			"username"			    : "insta_adarshnagar",
			"password"		        : "123456",
			"Outletname" 			: "Adarsh Nagar, Jalandhar",
			"latitude"              : "31.32990749999999",
			"longitude"             : "75.56381729999998",
			"address"               : "Punjab 144002, India",
			"city"                  : "1",
			"area"                  : "1",
			"pincode"				: "123654",
			"gst"					: "07AADCI7733E1ZN"
		}

		Response: {

			"success": True,
			"message": "Outlet is registered successfully under your brand!!"
		}

		update outlets
		Data Post: {
			"id"                    :  "i8"
			"Outletname" 			: "Adarsh Nagar, Jalandhar1",
			"latitude"              : "31.32990749999999",
			"longitude"             : "75.56381729999998",
			"address"               : "Punjab 144002, India",
			"city"                  : "1",
			"area"                  : "1",
			"pincode"				: "123456",
			"gst"					: "07AADCI7733E1ZN"
		}

		Response: 	{
					"success": true,
					"message": "successflly updated!!"
				}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			auth_id = request.user.id
			# user = auth_id
			cid = get_user(auth_id)
			record = OutletProfile.objects.filter(Company=cid)
			if record.count() == 0:
				data['priority'] = 1
			else:
				maxp = OutletProfile.objects.filter(Company=cid).aggregate(Max('priority'))
				priority = maxp['priority__max']
				data['priority'] = priority + 1
			if "id" in data:
				outlet_name_check = \
					OutletProfile.objects.filter(~Q(id=data["id"]),\
									Q(Outletname__iexact=data["Outletname"]))
			else:
				outlet_name_check = \
					OutletProfile.objects.filter(Q(Outletname__iexact=data["Outletname"]))
			if outlet_name_check.count() == 1:
				err_message = {}
				err_message["Outletname"] = \
					"Outlet with this name already exists..Please try other!!"
				return Response({
					"success"	: 	False,
					"error"		: 	err_message,
					"message"	: 	"Please correct listed errors!!"
				})
			else:
				pass
			if "id" in data:
				validation_check = err_check_update(data)
				if validation_check != None:
					return Response(validation_check)
				err_message = {}
				if data['id'] != '':
					Outlet_record = OutletProfile.objects.filter(id=data['id'])
					if Outlet_record.count() == 0:
						return Response(
							{
								"success"	: 	False,
								"message"	: 	"Outlet data is not valid to update!!"
							}
						)
					else:
						Outlet_record.update(Outletname = data['Outletname'],latitude = data['latitude'],longitude=data['longitude'],
											 address = data['address'],city = data['city'],area = data['area'],
											 updated_at = datetime.now(),pincode=data['pincode'],\
											 gst=data["gst"])

						return Response({
							"success"	: 	True,
							"message"	: 	"Profile successfully updated!!"
						})
				else:
					err_message["outlet"] = "Outlet is not valid!!"
					return Response({
						"success"	: 	False,
						"error" 	: 	err_message,
						"message" 	: 	"Please correct listed errors!!"
						})

			else:
				validation_check = err_check(data)
				if validation_check != None:
					return Response(validation_check)
				user_already_exist = User.objects.\
						filter(username=data['username'])
				if user_already_exist.count() == 1:
					err_message = {}
					err_message['user'] = "Outlet with this username already exists!!"
					return Response({
						"success"	: 	False,
						"error" 	: 	err_message,
						"message" 	: 	"Please correct listed errors!!"
						})
				else:
					pass
				company_query = Company.objects.filter(id=cid)
				if company_query.count() != 0:
					data["Company"] = company_query[0].id
				else:
					return Response(
						{
							"success"	: 	False,
							"message"	: 	"Company is not valid!!"
						}
					)
				create_user = User.objects.create_user(
						username=data['username'],
						password=data['password'],
						is_staff=False,
						is_active=True
						)
				if create_user:
					data["active_status"] = 1
					data["auth_user"] = create_user.id
					outlet_serializer = OutletSerializer(data=data)
					if outlet_serializer.is_valid():
						data_info = outlet_serializer.save()
						outlet_id = data_info.id
						start_new_thread(map_products_to_outlet, (outlet_id,data["company_auth_id"]))
						return Response(
									{
							"success": True,
							"message": "Outlet is registered successfully under your brand!!"
									}
									)
					else:
						return Response(
						{
						"success": False, "message": str(outlet_serializer.errors)
							}
							)
				else:
					return Response(
					{
					"success": False,
					"message": "Some error occured in the process of outlet manager creation!!"
					}
					)
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


class OutletRetreiveSerializer(serializers.ModelSerializer):
	class Meta:
		model = OutletProfile
		exclude = ['password']

class OutletRetreive(APIView):
	"""
		Outlet Retreive POST API

			Authentication Required		: Yes
			Service Usage & Description	: This Api is used to Retreive  outlets within brand.

			Data Post: {

				"id"  : "18"
			}

			Response: {
					"success": true,
					"data": [
						{
							}
					],
					"message": "successfully retreive the data"
				}

		"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			if data['id'] != '':
				Outlet_record = OutletProfile.objects.filter(id=data['id'])
				serializer = OutletRetreiveSerializer(Outlet_record,many=True)
				return Response({"success": True,
								 "data" : serializer.data,
								 "message": "successfully retreive the data"})
			else:
				return Response({"success": False,
								 "message": "please check user id"})

		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
