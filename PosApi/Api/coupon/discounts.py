from rest_framework.views import APIView
from rest_framework.response import Response
from Product.models import ProductCategory, Product_availability, Category_availability, Product,\
Variant,AddonDetails
from ZapioApi.api_packages import *
from django.db.models import Q
from rest_framework_tracking.mixins import LoggingMixin
import datetime
from discount.models import Coupon
from frontApi.coupon.coupon_check import *
from rest_framework.permissions import IsAuthenticated

class CouponcodeView(LoggingMixin,APIView):
	"""
	Coupon Code POST API

		Authentication Required		: yes
		Service Usage & Description	: This Api is used Coupon discount on the basis of provided 
		Coupon code,

		Data Post: {
			"coupon_code":"FLAT150",
			"outlet":"1",
			"cart":[
			  {
				"name": "The Destroyer",
				"details": {
				  "price": 919,
				  "actualPrice": 839,
				  "content": "The undisputed champion with all our meats (pork and chicken) with extra cheese on the house. No BS!"
				},
				"type": "Non-Veg",
				"image": "https://zapio-admin.com/media/product_image/Cheese_Bomb_Deep_Dish_iyyhxu_HMr3bnq.jpg",
				"id": 8,
				"quantity": 1,
				"customizable": true,
				"taxes": [
				  {
					"name": "SGST",
					"value": 2.5
				  },
				  {
					"name": "CGST",
					"value": 2.5
				  }
				],
				"toppings": {
				  "id": 127,
				  "addons": [
					{
					  "name": "Cheese 8 DD",
					  "price": 80
					},
					{
					  "name": "Cracked Black Pepper",
					  "price": 0
					},
					{
					  "name": "Green Chillies",
					  "price": 0
					},
					{
					  "name": "Red Paprika",
					  "price": 0
					},
					{
					  "name": "Jalapeno",
					  "price": 0
					}
				  ],
				  "crust": "8 inches",
				  "crustPrice": 839
				}
			  },
			  {
				"name": "Veg Bagel Bombs",
				"details": {
				  "price": 160,
				  "actualPrice": 160,
				  "content": null
				},
				"type": "Veg",
				"image": "https://zapio-admin.com/media/",
				"id": 191,
				"quantity": 1,
				"customizable": false,
				"taxes": [
				  {
					"name": "SGST",
					"value": 2.5
				  },
				  {
					"name": "CGST",
					"value": 2.5
				  }
				]
			  },
			  {
				"name": "Non-Veg Garlic Twist",
				"details": {
				  "price": 119,
				  "actualPrice": 119,
				  "content": null
				},
				"type": "Non-Veg",
				"image": "https://zapio-admin.com/media/",
				"id": 190,
				"quantity": 1,
				"customizable": false,
				"taxes": [
				  {
					"name": "SGST",
					"value": 2.5
				  },
				  {
					"name": "CGST",
					"value": 2.5
				  }
				]
			  },
			  {
				"name": "2 Chocolate Chip Cookies",
				"details": {
				  "price": 99,
				  "actualPrice": 99,
				  "content": "Instapizza's favourite chocolate chip cookies - 2 pieces"
				},
				"type": "Veg",
				"image": "https://zapio-admin.com/media/product_image/Dark_Chunk_Cookie_vmdqyl.jpg",
				"id": 53,
				"quantity": 1,
				"customizable": true,
				"taxes": [
				  {
					"name": "SGST",
					"value": 2.5
				  },
				  {
					"name": "CGST",
					"value": 2.5
				  }
				],
				"toppings": {
				  "id": 53,
				  "addons": [],
				  "crust": "Drinks & Desserts",
				  "crustPrice": 99
				}
			  }
			]
			}

		Response: {
				{
					"status": true,
					"subtotalprice": 1396
				}
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data  = request.data
			ccode = data['coupon_code']
			outlet = data['outlet']
			today = datetime.datetime.now()
			if ccode !="":
				err_message = {}
				err_message["outlet"] = validation_master_anything(str(outlet),
				"Outlet id",contact_re, 1)
				if any(err_message.values())==True:
					return Response({
						"success": False,
						"error" : err_message,
						"message" : "Please correct listed errors!!"
						})
				query = Coupon.objects.filter(coupon_code__exact=ccode,frequency__gte=1,
							valid_till__gte=today)
				if len(query[0].outlet_id) > 0:
					query = Coupon.objects.filter(frequency__gte=1,coupon_code__exact=ccode,
							valid_till__gte=today,outlet_id__icontains=str(data["outlet"]))
					if query.count() > 0:
						apply_coupon = check_coupon(data,ccode)
						subtotalprice = apply_coupon["subtotalprice"]
						Old_subtotal = apply_coupon["Old_subtotal"]
						coupon_applied = apply_coupon["coupon_applied"]
						tdaprice = apply_coupon["tdaprice"]
						tax = subtotalprice * 5 / 100
						aprice = subtotalprice + tax
						if coupon_applied == 1:
							return Response({"status":True,
											"Old_subtotal" : Old_subtotal,
											"new_subtotal" : subtotalprice,
											"Discount_value" : tdaprice,
											"Tax" : tax,
										"total_value":aprice})
						else:
							return Response({"status":False,
										"message":"Applied coupon code is invalid!!"})
		  
					else:
						return Response({"status":False,
						   "message":"Applied coupon code is not valid for outlet!!"})
				else:
					apply_coupon = check_coupon(data,ccode)
					subtotalprice = apply_coupon["subtotalprice"]
					Old_subtotal = apply_coupon["Old_subtotal"]
					coupon_applied = apply_coupon["coupon_applied"]
					tdaprice = apply_coupon["tdaprice"]
					tax = subtotalprice * 5 / 100
					aprice = subtotalprice + tax
					if coupon_applied == 1:
						return Response({"status":True,
										"Old_subtotal" : Old_subtotal,
										"new_subtotal" : subtotalprice,
										"Discount_value" : tdaprice,
										"Tax" : tax,
									    "total_value":aprice})
					else:
						return Response({"status":False,
									"message":"Applied coupon code is invalid!!"})

			else:
				return Response({"status": False, 
								"message": "Coupon Code is not provided!!"})
		except Exception as e:
			print("CoupondataApiException")
			print(e)
			return Response({"status": False, 
							"message": "Bad Request", 
							 "error": str(e)})