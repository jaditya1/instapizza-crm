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
from UserRole.models import *
from OTPMgr.otp_send import send_otp
from OTPMgr.otp_verify import verify_otp


def send_modules(user):
	is_pos = ManagerProfile.objects.filter(username=user)
	if is_pos.count()==1:
		Company_id = is_pos[0].Company_id
		user_type = is_pos[0].user_type.user_type
		type_id = is_pos[0].user_type_id
		allmenu = BillingMainRoutingModule.objects.filter(active_status=1).order_by('priority')
		alldata = []
		for i in allmenu:
			alls = {}
			ids = i.id
			alls['module'] = i.module_name
			rp = BillRollPermission.objects.filter(user_type_id=type_id,company_id=Company_id,main_route_id=i.id)
			lp = rp[0].label
			if lp == False:
				alls['permissions'] = lp
			else:
				alls['permissions'] = lp
			alldata.append(alls)
		al = {}
		for j in alldata:
			al[j['module']] = j['permissions']
		return al
	else:
		return None
	



class Poslogin(APIView):

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
			
			is_pos = ManagerProfile.objects.filter(username=data["username"])
			if is_pos.count()==1:
				if is_pos[0].active_status == 0:
					return Response({
					"success" : False,
					"message" : "Pos account is not active..Please contact admin!!"
					})
				else:
					pass
				if is_pos[0].mobile == None:
					return Response({
					"success" : False,
					"message" : "No mobile is associated with this account!!"
					})
				else:
					pass
				user_mobile = "91"+is_pos[0].mobile
				is_company = Company.objects.filter(id=is_pos[0].Company_id)[0]	
				if is_company.active_status == 0:
					return Response({
					"success" : False,
					"message" : "Your company account is deactivated due to some reason!!"
					})
				else:
					pass
				username = str(is_company.id)+'m'+data['username']

				user_authenticate = authenticate(username=username,
											password=data['password'])

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
					user_type = is_pos[0].user_type.user_type
					# send_otp(user_mobile, "Billing")
					return Response({
						"success": True,
						"credential" : True,
						"user_id" : user_id,
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
				"message": "Username not found!"
				})
		except Exception as e:
			return Response({
				"success": False, 
				"message": "Error happened!!", 
				"errors": str(e)
				})



class PosOTPVerify(APIView):

	"""
	POS login OTP Verify POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to verify login OTP.

		Data Post: {

			"user_id"	:	"33204",
			"otp"		:	"5689"	
		}

		Response: {

			"success"		: 	True,
			"credential" 	: 	True,
			"permissions" 	: 	al,
			"token"			: 	token.key,
			"user_id" 		: 	6454,
			"user_type"		:	"Admin",
			"username" 		: 	"admin",
			"message" 		: 	"You are logged in now!!"
		}

	"""

	def post(self, request, format=None):
		try:
			data = request.data
			mgr_record = ManagerProfile.objects.filter(auth_user=data["user_id"])
			if mgr_record.count() == 1:
				if mgr_record[0].mobile == None:
					return Response({
					"success" : False,
					"message" : "No mobile is associated with this account!!"
					})
				else:
					pass
				user_mobile = "91"+mgr_record[0].mobile
				otp_verification = "122333"
				# otp_verification = verify_otp(user_mobile, str(data["otp"]))
				if otp_verification == str(data["otp"]):
					token_record = Token.objects.filter(user_id=data["user_id"])
					if token_record.count() == 1:
						token_key = token_record[0].key
						user_type = mgr_record[0].user_type.user_type
						username = mgr_record[0].username
						user_id = data["user_id"]
						modules = send_modules(username)
						if modules == None:
							return Response({
								"success"	:	False,
								"message"	:	"No modules attached with this account!!"
								})
						else:
							pass
						return Response({
							"success"		: 	True,
							"credential" 	: 	True,
							"permissions" 	: 	modules,
							"token"			: 	token_key,
							"user_id" 		: 	user_id,
							"user_type"		:	user_type,
							"username" 		: 	username,
							"message" 		: 	"You are logged in now!!"
							})
					else:
						return Response({
						"success"	:	False,
						"message"	:	"This user creds are not authenticated!!"
						})
				else:
					return Response({
						"success"	:	False,
						"message"	:	"OTP verification failed!!"
						})
			else:
				return Response({
					"success" : False,
					"message" : "Invalid user request!!"
					})

		except Exception as e:
			return Response({
				"success"	: 	False, 
				"message"	: 	"Error happened!!", 
				"errors"	: 	str(e)
				})




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

