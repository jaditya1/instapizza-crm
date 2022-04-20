from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingMixin

from ZapioApi.api_packages import *
from frontApi.order.error_radious_check import check_circle
from Outlet.models import OutletProfile
from rest_framework.permissions import IsAuthenticated


class ServiceCheck(LoggingMixin,APIView):
	"""
	Service Check POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to check address is servicable or not.

		Data Post:  {

			"address": {
						"city":"Greater Noida",
						"state":"UP",
						"address":"Fusion Homes",
						"pincode":"152365",
						"landmark":"Teen Murti",
						"latitude":28.5995288,
						"longitude":77.44454669999999
						},
			"outlet_id" : 3
		}

		Response: {

			"success": true,
			"message": "Order Received successfully"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			shop_check = OutletProfile.objects.filter(id=data['outlet_id'])
			err_message = {}
			address = data["address"]
			if "city" in address:
				err_message["City"] = \
				only_required(address['city'], "City")
			else:
				err_message["City"] = "City is not provided in address!!"

			if "state" in address:
				err_message["state"] = \
					only_required(address['state'], "state")
			else:
				err_message["state"] = "State is not provided in address!!"
			if "latitude" in address:
				err_message["latitude"] = \
					only_required(str(address['latitude']), "latitude")
			else:
				err_message["latitude"] = "Latitude is required in address!!"
			if "longitude" in address:
				err_message["longitude"] = \
				only_required(str(address['longitude']), "longitude")
			else:
				err_message["longitude"] = "Longitude is required in address!!"
			if "address" in address:
				err_message["address"] = \
					only_required(address['address'], "address")
			else:
				err_message["address"] = "Address is not provided!!"
			if 'landmark' in address:
				err_message["landmark"] = \
					only_required(address['landmark'], "landmark")
			else:
				pass
			if "pincode" in address:
				err_message["pincode"] = \
				only_required(address['pincode'], "pincode")
			else:
				err_message["pincode"] = "Pincode is not provided in address!!"
			if any(err_message.values())==True:
				return Response({
								"success": False,
								"error" : err_message,
								"message" : "Please correct listed errors!!"
							})

			distance_check = {}
			distance_check["shop_id"] = data["outlet_id"]
			distance_check["lat"] = address["latitude"]
			distance_check["long"] = address["longitude"]

			service_check = check_circle(distance_check)
			if service_check == None:
				return Response({
					"success"	:	True,
					"message"	:	"Address is servicable!!"
					})
			else:
				return Response(service_check)
		except Exception as e:
			return Response({
							"success"	: 	False,
							"message"	:	"Service Check api stucked into exception!!",
							"error" 	:	str(e) 
							})