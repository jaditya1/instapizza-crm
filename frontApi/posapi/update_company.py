from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
from django.db.models import Q
import os
from django.db.models import Max
from rest_framework import serializers
import requests
from pos.models import POSOrder
from datetime import datetime, timedelta
import time
import dateutil.parser

class POSSerializer(serializers.ModelSerializer):

	class Meta:
		model = POSOrder
		fields = '__all__'


class UpdateCompany(APIView):
	"""
	POS data POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to update company id.

		Data Post: {

		}

		Response: {
		}
	"""

	def post(self, request, format=None):
		try:
			data = {}
			alldata1 = POSOrder.objects.filter()
			data['company'] = 1
			for i in alldata1:
				if i.company_id == None:
					print(i.id)
					alls = POSOrder.objects.filter(id=i.id)
					aa = POSSerializer(alls[0],data=data,partial=True)
					if aa.is_valid():
						aa.save()
						print("eeeeeeeeee")
					else:
						print(aa.errors)
				else:
					pass
			return Response({"success": True, 
							"message": "Save Successfully", 
								})
		except Exception as e:
			print("POS data creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, 
							"message": "Error happened!!", 
							"errors": str(e)})


