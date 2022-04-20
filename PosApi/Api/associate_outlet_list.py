from rest_framework.views import APIView
from rest_framework.response import Response
from Brands.models import Company
from UserRole.models import ManagerProfile
from django.db.models import Q

def company_type(company_id):
	outlet = []
	if company_id == 1:
		record = ManagerProfile.objects.filter()
	else:
		return "normal"