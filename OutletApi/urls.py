from django.urls import path
from OutletApi.Api.Authorization.create_update_delivery import (DeliveryAction,
																DeliveryBoyRegistration,
																DeliveryBoyListing,
																DeliveryBoyRetrieval,
																DeliveryActiveListing)

from OutletApi.Api.order.listing import  OrderListingData
from OutletApi.Api.order.change_order_status import  ChangeStatusData
from OutletApi.Api.order.retrieve_order import  OrderRetrieval
from OutletApi.Api.Authorization.profile import  OutletRetrieve

from OutletApi.Api.Authorization.onoff import  outletOnOff, Outlet_Is_open

from OutletApi.Api.listing.product import Productlist
from OutletApi.Api.listing.category import Categorylist
from OutletApi.Api.availability.product import Productavail
from OutletApi.Api.availability.category import Category

# 

urlpatterns = [
	#API Endpoints for Delivery Boy Registration
	path('deliveryboy/registration/',DeliveryBoyRegistration.as_view()),
	path('deliveryboy/listdata/',DeliveryBoyListing.as_view()),
	path('action/DeliveryBoy/',DeliveryAction.as_view()),
	path('activeListing/DeliveryBoy/',DeliveryActiveListing.as_view()),
	path('retrieval_data/delivery_boy/',DeliveryBoyRetrieval.as_view()),

	#API Endpoints for order 
	# path('order/',OrderData.as_view()),
	path('orderlisting/',OrderListingData.as_view()),
	path('orderStatuschange/',ChangeStatusData.as_view()),
	path('retrievalOrder/',OrderRetrieval.as_view()),
	path('retrieve/outlet/', OutletRetrieve.as_view()),

	#API used For open / close outlet
	path('onoff/',outletOnOff.as_view()),

	#API enspoints for product & category listing
	path('listing/product/',Productlist.as_view()),
	path('listing/category/',Categorylist.as_view()),

	# API endpoints for availability
	path('availability/product/',Productavail.as_view()),
	path('availability/Category/',Category.as_view()),

	# API ENDPOINT for outlet open status
	path('is_open/',Outlet_Is_open.as_view()),


]

