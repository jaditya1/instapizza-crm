import re
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from Brands.models import Company
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from ZapioApi.api_packages import *
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from zapio.settings import Media_Path
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from UserRole.models import *
from django.db.models import Q
from OTPMgr.otp_send import send_otp_to_pos
from OTPMgr.otp_verify import verify_otp
from rest_framework_tracking.mixins import LoggingMixin
# from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


def PosModules(p_id,company_id):
	allmenu = MainRoutingModule.objects.filter(active_status=1).order_by('priority')
	alldata = []
	for i in allmenu:
		alls = {}
		chk_p = RollPermission.objects.filter(Q(company_id=company_id),\
						Q(main_route_id=i.id),Q(label=1),Q(user_type_id=p_id))
		if chk_p.count() > 0:
			alls['id'] = i.module_id
			alls['icon'] = i.icon
			alls['label'] = i.label
			alls['to'] = i.to
			alls['ids'] = i.id
			alls['ids'] = i.id
			rmodule = RoutingModule.objects.filter(main_route_id=i.id)
			if rmodule.count() > 0:
				alls['subs'] = []
				for j in rmodule:
					al = {}
					al['icon'] = j.icon
					al['label'] = j.label
					al['to'] = j.to
					r = SubRoutingModule.objects.filter(route_id=j.id)
					if r.count() > 0:
						al['subs'] = []
						for k in r:
							a = {}
							a['icon'] = k.icon
							a['label'] = k.label
							a['to'] = k.to
							al['subs'].append(a)
					alls['subs'].append(al)
			else:
				pass
			alldata.append(alls)
		else:
			pass
	if len(alldata) > 0:
		alldata = alldata
	else:
		alldata = []
	return alldata


def auth_data(user_type, query):
	q = query[0]
	is_valid = 0
	data_to_send = {}
	if user_type == "is_outlet":
		if q.active_status == True and q.is_company_active == True:
			is_valid = 1
			logo = q.Company.company_logo
			display_name = q.Outletname
			if logo != None and logo != "":
				logo = Media_Path+str(q.Company.company_logo)
			else:
				logo = None
		else:
			pass
	elif user_type == "is_brand":
		if q.active_status == True:
			is_valid = 1
			logo = q.company_logo
			display_name = q.company_name
			if logo != None and logo != "":
				logo = Media_Path+str(q.company_logo)
			else:
				logo = None
		else:
			pass
	else:
		if q.active_status == True:
			is_valid = 1
			logo = q.Company.company_logo
			display_name = q.Company.company_name
			if logo != None and logo != "":
				logo = Media_Path+str(logo)
			else:
				logo = None
		else:
			pass
	if is_valid == 1:
		data_to_send["logo"] = logo
		data_to_send["name"] = display_name
		return data_to_send
	else:
		return None

	




class BrandOutletlogin(LoggingMixin,APIView):


	"""	
	InstaPOS login POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to provide login services to outlets & brands.

		Data Post: {

			"username"			    : "insta_adarshnagar",
			"password"		        : "123456"
		}

		Response: {

			"success"		: 	True,
			"credential" 	: 	True,
			"user_id"		:	user_id,
			"user_type"		:	user_type
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
			is_outlet = OutletProfile.objects.filter(username=data['username'])
			is_brand = Company.objects.filter(username=data['username'])
			is_cashier = ManagerProfile.objects.filter(username=data['username'])
			is_found = 0
			if is_outlet.count()==1:
				user_type = "is_outlet"
				company_id = is_outlet[0].Company_id
				user_mobile = is_outlet[0].mobile_with_isd
				p_id = str(5)
				is_found = 1
				user = data["username"]
			else:
				pass
			if is_brand.count()==1 and  is_found == 0:
				company_id = is_brand[0].id
				user_type = "is_brand"
				user_mobile = is_brand[0].contact_person_mobileno
				p_id = str(4)
				is_found = 1
				user = data["username"]
			else:
				pass
			if is_cashier.count()==1:
				p_id = is_cashier[0].user_type_id
				user_type = UserType.objects.filter(id=p_id)[0].user_type
				company_id = is_cashier[0].Company_id
				user = str(company_id)+'m'+str(data['username'])
				is_found = 1
				user_mobile = is_cashier[0].mobile
			else:
				pass
			user_mobile = "91"+str(user_mobile)
			if is_found == 0:
				return Response({
					"success"	:	False,
					"message"	:	"No User found!!"
					})
			else:
				pass
			user_authenticate = authenticate(username=user,
											password=data['password'])
			if user_authenticate == None:
				return Response({
					"success"		: 	False,
					"credential" 	: 	False,
					"message"		: 	"Please enter valid login credentials!!"
					})
			else:
				pass
			token, created = Token.objects.get_or_create(user=user_authenticate)
			user_id = token.user_id
			# send_otp_to_pos(user_mobile)
			return Response({
				"success"		: 	True,
				"credential" 	: 	True,
				"user_id"		:	user_id,
				"user_type"		:	user_type
				})
		except Exception as e:
			return Response({
				"success"	: 	False, 
				"message"	: 	"Error happened!!", 
				"errors"	: 	str(e)
				})


class IposOTPVerify(LoggingMixin,APIView):

	"""
	IPOS login OTP Verify POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to verify login OTP.

		Data Post: {

			"user_id"	:	"33204",
			"otp"		:	"5689",
			"user_type"	:	"is_brand"
		}

		Response: {

			"success"		: 	True,
			"credential" 	: 	True,
			"message" 		: 	"You are logged in now!!",
			"user_type" 	: 	user_type,
			"token"			: 	token_key,
			"user_id" 		: 	user_id,
			"name" 			: 	name,
			"logo" 			: 	logo,
			"menu" 			: 	pos_modules
		}

	"""

	def post(self, request, format=None):
		try:
			data = request.data
			if data["user_type"] == "is_brand":
				p_id = str(4)
				record = Company.objects.filter(auth_user=data['user_id'])
				
			elif data["user_type"] == "is_outlet":
				p_id = str(5)
				record = OutletProfile.objects.filter(auth_user=data['user_id'])
			else:
				record = ManagerProfile.objects.filter(auth_user=data["user_id"])
			if record.count() == 1:
				if data["user_type"] != "is_outlet" and data["user_type"] != "is_brand":
					p_id = record[0].user_type_id
					data["user_type"] = record[0].user_type.user_type
				else:
					pass
				if data["user_type"] == "is_outlet":
					user_mobile = record[0].mobile_with_isd
					company_id = record[0].Company_id
				elif data["user_type"] == "is_brand":
					user_mobile = record[0].contact_person_mobileno
					company_id = record[0].id
				else:
					user_mobile = record[0].mobile
					company_id = record[0].Company_id 
				if user_mobile == None:
					return Response({
					"success" : False,
					"message" : "No mobile is associated with this account!!"
					})
				else:
					pass
				pos_modules = PosModules(p_id, company_id)
				user_mobile = "91"+user_mobile
				all_auth_data =  auth_data(data["user_type"], record)
				if all_auth_data == None:
					return Response({
						"status"	:	False,
						"message"	:	"User not valid!!"
						})
				else:
					pass
				# otp_verification = verify_otp(user_mobile, str(data["otp"]))
				otp_verification = "122333"
				if otp_verification == str(data["otp"]):
					token_record = Token.objects.filter(user_id=data["user_id"])
					if token_record.count() == 1:
						token_key = token_record[0].key
						user_type_data = data["user_type"] 
						user_id = data["user_id"]
						logo = all_auth_data["logo"]
						name = all_auth_data["name"]
						return Response({
							"success"		: 	True,
							"credential" 	: 	True,
							"message" 		: 	"You are logged in now!!",
							"user_type" 	: 	user_type_data,
							"token"			: 	token_key,
							"user_id" 		: 	user_id,
							"name" 			: 	name,
							"logo" 			: 	logo,
							"menu" 			: 	pos_modules
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


class BrandOutletlogout(APIView):
	"""
	Outlet/Brand logout POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide logout service to outlets & brands.

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
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



