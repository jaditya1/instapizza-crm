from django.urls import path
from withrun.Api.OrderData import OrdersDetail


urlpatterns = [

	path('orderdata/',OrdersDetail.as_view()),
]