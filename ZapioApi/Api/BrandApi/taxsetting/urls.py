from django.urls import path, include
from .activetax import ActiveTaxlisting


urlpatterns = [

	path('activetax/listing/',ActiveTaxlisting.as_view()),
]