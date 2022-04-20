from django.urls import path, include
from MicroApi.Api.Authorization.login import Micrologin,Micrologout

urlpatterns = [
	path('login/',Micrologin.as_view()),
	path('logout/',Micrologout.as_view()),

]


