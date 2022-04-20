from django.urls import path
from dashboardApi.Api.rhi_report import dashboardRHI
from dashboardApi.Api.order_report import dashboardOrder


urlpatterns = [
	#API Endpoints for brand dashboard
	path('outlet/rhiReport/',dashboardRHI.as_view()),
	#API Endpoints for outlet dashboard
	path('outlet/orderReport/',dashboardOrder.as_view()),

]