from rest_framework.views import APIView
from rest_framework.response import Response
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
from UserRole.models import ManagerProfile,UserType
from zapio.settings import Media_Path



class AutomaticLogin(APIView):

	"""	
	Pos login POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to provide login services to pos.

		Data Post: {

			"username"			    : "umesh",
			"password"		        : "123456"
		}

		Response: {

			    "success": true,
			    "credential": true,
			    "message": "You are logged in now!!",
			    "user_type": "Pos Manager",
			    "token": "5f7b5a511109b961e534604db0899910e354ee95",
			    "user_id": 150
		}

	"""
	

	def post(self, request, format=None):
		try:
			data = request.data
			err_message = {}
			pos = ManagerProfile.objects.filter(user_type__user_type__iexact="pos manager")
			username = pos[0].username
			password = pos[0].password
			is_pos = ManagerProfile.objects.filter(username=username,
								user_type__user_type__iexact="pos manager")
			if is_pos.count() > 0:
				user_type = is_pos[0].user_type.user_type
			else:
				return Response({
						"success": False,
						"message": "Username not found!"
						})
			if is_pos.count() > 0:
				if is_pos[0].active_status == 0:
					return Response({
					"success" : False,
					"message" : "Pos account is not active..Please contact admin!!"
					})
				else:
					pass
				is_company = Company.objects.filter(id=is_pos[0].Company_id)[0]	
				if is_company.active_status == 0:
					return Response({
					"success" : False,
					"message" : "Your company account is deactivated due to some reason!!"
					})
				else:
					pass
				credential_check = \
					is_pos.filter(password=password)
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
				username = str(is_company.id)+'m'+username
				user_authenticate = authenticate(username=username,
											password=password)
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
					pro_pic = is_pos[0].manager_pic
					full_path = Media_Path
					if pro_pic != None and pro_pic != "":
						pic = full_path+str(pro_pic)
					else:
						pic = None
					return Response({
						"success": True,
						"credential" : True,
						"message" : "You are logged in now!!",
						"user_type" : user_type,
						"token": token.key,
						"user_id" : user_id,
						"profile_pic" : pic
						})
				else:
					return Response({
						"success": False,
						"credential" : False,
						"message": "Please enter valid login credentials!!"
						})

			else:
				pass

		except Exception as e:
			print("POS Login Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class Poslogout(APIView):
	"""
	POS logout POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide logout service to pos.

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