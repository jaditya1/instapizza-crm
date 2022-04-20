from django.urls import path
from Dunzo.Api.dunzo_services import GetQuote, OrderAddressCustomerUpdate, \
						OrderTaskStatus, WebhookTaskStateUpdate


urlpatterns = [

	path('GetQuote/',GetQuote.as_view()),
	path('OrderAddressCustomerUpdate/',OrderAddressCustomerUpdate.as_view()),
	# path('OrderTask/',OrderTask.as_view()),
	path('OrderTaskStatus/',OrderTaskStatus.as_view()),
	path('WebhookTaskStateUpdate/',WebhookTaskStateUpdate.as_view()),

]
