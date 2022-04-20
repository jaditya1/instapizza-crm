import re
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from microservice.models import Microservice
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from ZapioApi.api_packages import *
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class Micrologin(APIView):

	"""	
	Brand login POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to provide login services to  brands.

		Data Post: {

			"username"			    : "umeshsamal",
			"password"		        : "123456789"
		}

		Response: {

			"success"				: true,
			"credential"			: true,
			"message"				: "You are logged in now!!",
			"user_type"				: "is_outlet",
			"token"					: "1614ffa75cb577542c76ae4ad6ea146b61d688fc",
			"user_id"				: 6
		}

	"""
	
	# permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			err_message = {}
			err_message["username"] =  validation_master_anything(
									data["username"],
									"Username", username_re, 3)

			err_message["password"] =  only_required(data["password"],"Password")

			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})

			is_brand = Microservice.objects.filter(username=data['username'])

			if is_brand.count()==1:
				user_type = "is_brand"
			else:
				pass

			if is_brand.count()==1:
				if is_brand.first().active_status == 0:
					return Response({
					"success" : False,
					"message" : "Company account is not active..Please contact admin!!"
					})
				else:
					pass
				credential_check = \
					is_brand.filter(password=data['password'])

				if credential_check.count() == 1:
					pass
				else:
					return Response \
						({
						"success": False,
						"credential" : False,
						"message": \
						"Please enter valid login credentials!!"
						})
				user_authenticate = authenticate(username=data['username'],
											password=data['password'])
				brand = is_brand[0].company.id

				if user_authenticate == None:
					return Response({
						"success": False,
						"credential" : False,
						"message": "Your account is not activated, please open your registered email!!"
						})
				else:
					pass
				if user_authenticate and user_authenticate.is_active == True \
										and user_authenticate.is_staff==False\
										and user_authenticate.is_superuser == False:
					login(request,user_authenticate)
					token, created = Token.objects.get_or_create(user=user_authenticate)
					user_id = token.user_id
	
					return Response({
						"success": True,
						"credential" : True,
						"message" : "You are logged in now!!",
						"token": token.key,
						"user_id" : user_id,
						"company_id" : brand,

						})
				else:
					return Response({
						"success": False,
						"credential" : False,
						"message": "Please enter valid login credentials!!"
						})
			else:
				return Response({
						"success": False,
						"credential" : False,
						"message": "This Username does not exist in the system!!"
						})
		except Exception as e:
			print("Brand Login Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class Micrologout(APIView):
	"""
	Outlet/Brand logout POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide logout service to brands.

		Data Post: {

			"token": "95dabfce1f8ebe9331851a1a1c5aa22bcb9b8120"
		}

		Response: {

			"success": True,
			"message" : "You have been successfully logged out!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			self.authuserId = request.user.id
			userData = User.objects.filter(id=self.authuserId).first()
			if userData:
				request.user.auth_token.delete()
				logout(request)
				return Response({
							"success": True,
							"message": "You have been successfully logged out!!",
							})
			else:
				return Response({
							"success": False,
							"message": "User not Found!!",
							})
		except Exception as e:
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})