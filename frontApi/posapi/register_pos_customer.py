from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from Brands.models import Company
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import re
from ZapioApi.api_packages import *
import datetime
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from pos.models import POSOrder
from CustomerApi.serializers.customer_serializer import CustomerSignUpSerializer,CustomerOTPSerializer
from Customers.models import CustomerProfile


class Register(APIView):

	"""
	Customer Registration  POST API

		Authentication Required		: No

		Service Usage & Description	: This Api is used to register customer

		Data Post: {

			"email": "umeshsamal3@gmail.com",
			"mobile": "8585858585",
			"password": "123456",
			"refercode" : "24240951"
			
			}

		Response: {

		   "success": true,
		   "customer_id": 4,
		   "message": "You have been registered successfully..A confirmation OTP has been sent on your email id!!"

		}

	"""

	def post(self, request, format=None):
		try:
			password = '12345678'
			registration_data = {}
			alldata = POSOrder.objects.filter()
			for i in alldata:
				cnumber = i.customer_number
				if cnumber == None:
					pass
				else:
					a = cnumber.replace("#", "",)
					username = str(1)+ a
					user_already_exist = User.objects.filter(username=username)
					if user_already_exist.count() > 0:
						e = user_already_exist[0].id
						#print("eeeeeeeeeee",e)
						registration_data["name"] = i.customer_name
						registration_data["username"] = username
						registration_data["company"] = 1
						registration_data["mobile"] = a
						cus = CustomerProfile.objects.filter(auth_user_id=e)
						if cus.count() > 0:
							customer_registration_serializer = CustomerSignUpSerializer(cus[0],data=registration_data,partial=True)
							if customer_registration_serializer.is_valid():
								customer_data_save = customer_registration_serializer.save()
							else:
								print("sddsa",customer_registration_serializer.errors)
						else:
							pass
					else:
						create_user = User.objects.create_user(
										username=username,
										email=username,
										password=password,
										is_staff=False,
										is_active=True
										)
						if create_user:
							registration_data["auth_user"] = create_user.id
							registration_data["is_pos"] = 1
							registration_data["username"] = username
							registration_data["pass_pin"] = password
							registration_data["name"] = i.customer_name
							registration_data["company"] = 1
							registration_data["mobile"] = a
							registration_data["active_status"] = 1
							customer_registration_serializer = CustomerSignUpSerializer(data=registration_data)
							if customer_registration_serializer.is_valid():
								customer_data_save = customer_registration_serializer.save()
							else:
								print(customer_registration_serializer.errors)
						else:
							pass
			return Response({"success" : True,
								"message" : "Data has been saved"})
		except Exception as e:
			print("Registration Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})

