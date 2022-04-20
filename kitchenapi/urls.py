from django.urls import path
from kitchenapi.listing.order import ProductWiseOrderListing
from kitchenapi.steps.retrieve import PreparationStepRetrieval
from kitchenapi.process.order_process import ProcessStartEnd

urlpatterns = [
	#API Endpoints for Kitchen
	path('listing/orderProductwise/',ProductWiseOrderListing.as_view()),
	path('retrieve/Productsteps/',PreparationStepRetrieval.as_view()),
	path('process/startEnd/',ProcessStartEnd.as_view())

]