import calendar
from datetime import datetime

from django.db.models import Q
from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from frontApi.serializer.restaurent_serializers import OutletDetailsSerializer
from Brands.models import Company
from googlegeocoder import GoogleGeocoder
from googlemaps import Client
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
from Location.models import CityMaster,AreaMaster
from rest_framework_tracking.mixins import LoggingMixin

class RestaurantMapView(LoggingMixin, APIView):
	"""
	Nearest Restaurant POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to find nearest outlet on the basis of provided lat & 
		long.City and area are optional, request can be made by assigning values in city and area 
		as blank.

		Data Post: {
		
			"latitude"	:	"41.90278349999999",
			"longitude"	:	"12.4963655",
			"city"		:	"1",   (Optional)
			"area"		:	"1",   (OPtional)
			"company"   :   "1"
		}

		Response: {

			"status"				: True,
			"nearest_restaurants"	: self.customer_nearest_restaurent,
			"message"				: "Your nearest restaurant are sent successfully"
		}

	"""

	def __init__(self):
		self.latitude = None
		self.longitude = None
		self.city = None
		self.area = None
		self.customer_location = None
		self.myLocation = None
		self.config_rule_name = None
		self.config_unloaded_miles = 0
		self.range_in_kilometer = None
		self.customer_nearest_restaurent = []
		self.response_api_message = None
		self.Errors = None
		self.Company = None

	def restaurant_miles_converter(self):
		self.customer_location = (self.latitude, self.longitude)

	def get_area_name(self,ida):
		area_name = AreaMaster.objects.filter(id=ida).first()
		return area_name.area

	def get_city_name(self,ida):
		city_name = CityMaster.objects.filter(id=ida).first()
		return city_name.city

	def merge_all_nearest_restaurents(self, restaurant, kilometers):
		try:
			restaurant_data = {}
			restaurant_data['id'] = restaurant.id
			restaurant_data['username'] = restaurant.username
			restaurant_data['Outletname'] = restaurant.Outletname
			restaurant_data['mobile_with_isd'] = restaurant.mobile_with_isd
			restaurant_data['distance'] = kilometers
			restaurant_data['address'] = restaurant.address
			restaurant_data['is_open'] = restaurant.is_open
			restaurant_data['area'] = self.get_area_name(restaurant.area_id)
			restaurant_data['city'] = self.get_city_name(restaurant.city.id)
			return restaurant_data, True
		except Exception as e:
			print("merge_all_nearest_restaurents_exception")
			print(e)
			return None, e



	def chk_open_restaurents(self, restaurant):
		try:
			print(restaurant)

		except Exception as e:
			print("merge_all_nearest_restaurents_exception")
			print(e)
			return None, e



	def restaurant_details_records(self):
		all_restaurant =\
		OutletProfile.objects.filter(active_status=1,is_open=1,
			Company=self.Company).order_by('latitude')
		if all_restaurant.count() > 0:
			self.Restaurants = OutletDetailsSerializer(all_restaurant, many=True).data
		else:
			return Response({"status": True,
							"message": "No restaurant Found!!",
							})

		self.restaurant_miles_converter()
		if self.customer_nearest_restaurent == []:
			nearest = {}
			for restaurant in self.Restaurants:
				restaurant_locations = (restaurant['latitude'], restaurant['longitude'])
				unloaded_mile = great_circle(self.customer_location, restaurant_locations).miles
				if unloaded_mile == None:
					unloaded_mile = 0
				else:
					kilometers = round((unloaded_mile / 0.62137119), 2)
					nearest[restaurant['username']] = kilometers
					a=min(zip(nearest.values(), nearest.keys()))
			from Outlet.models import OutletMilesRules
			chk_radius = OutletMilesRules.objects.filter(Company=self.Company)
			if chk_radius.count() > 0:
				circle_radius = OutletMilesRules.objects.filter(Company=self.Company)[0].unloaded_miles
				if a[0]<=circle_radius:
					allrestaurants = OutletProfile.objects.filter(username=a[1]).first()
					time = datetime.now().time()
					to_let = 0
					chk_com = OutletProfile.objects.filter(active_status=1,is_open=1,\
					Company=self.Company,id=allrestaurants.id).order_by('latitude')
					if chk_com.count() == 0:
						return "time_set_issue"
					else:
						pass
					open_time = chk_com[0].opening_time
					close_time = chk_com[0].closing_time
					if open_time > close_time:
						c_tmp = open_time
						open_time = close_time
						close_time = c_tmp
						if time > open_time and time < close_time:
							pass
						else:
							to_let = 1
					else:
						if time > open_time and time < close_time:
							to_let = 1
						else:
							pass
					if chk_com.count() > 0 and to_let == 1:
						pass
					else:
						return "s"
					nearest_restaurant, rest_error = self.merge_all_nearest_restaurents(allrestaurants,a[0])
					if nearest_restaurant:
						self.customer_nearest_restaurent.append(nearest_restaurant)
					else:
						self.customer_nearest_restaurent = []
				else:
					return Response({"status": True,
									 "message": "No restaurant Found",
									})
			else:
				return Response({"status": True,
								 "message": "Service area radius is not set for this company at super-admin level!!",
								})

	def post(self,request):
		from Outlet.models import OutletMilesRules
		try:
			self.latitude = request.data['latitude']
			self.longitude = request.data['longitude']
			self.Company = request.data['company']
			company_check = Company.objects.filter(id=self.Company,is_open=1)
			if company_check.count()==0:
				return Response({"status"  : True,
								 "message" : "Sorry we are closed now!!",
								})
			else:
				pass
			if self.longitude != "" and self.longitude != "":
				time = datetime.time(datetime.now())
				chk_com = OutletProfile.objects.filter(active_status=1,is_open=1,\
					Company=self.Company).order_by('latitude')
				if chk_com.count() > 0:
					pass
				else:
					return Response({"status": True,
								 "message": "No Company Found!!",
								})
				circle_radius = OutletMilesRules.objects.filter(Company=self.Company)
				if circle_radius.count() > 0:
					pass
				else:
					return Response({"status": True,
								 "message": "Service area radius is not set for this company at super-admin level!!",
								})
				a = self.restaurant_details_records()
				if a == "s":
					return Response({"status": False,
									    "message": "Restaurants is closed",
									})
				else:
					pass

				if self.customer_nearest_restaurent:
					return_json_response = {
						"status": True,
						"nearest_restaurants": self.customer_nearest_restaurent,
						"message": "Your nearest restaurant are send successfully"
					}
					return Response(return_json_response)
				return Response({"status": False,
								 "message": "No restaurant Found",
								 "range": self.range_in_kilometer})
			else:
				pass
		except Exception as e:
			print(e)