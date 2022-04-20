from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

class PasswordVerify(APIView):

	"""	
	Password verify POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to verify password after inactivity.

		Data Post: {

			"password"		        : "123456"
		}

		Response: {

			    "success": true,
			    "credential": true
		}

	"""
	
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			username = request.user
			user_authenticate = authenticate(username=username,
											password=data['password'])

			if user_authenticate == None:
					return Response({
						"success"		: 	False,
						"credential" 	: 	False,
						"message"		: 	"Please enter valid login credentials!!"
						})
			else:
				pass
			if user_authenticate and user_authenticate.is_active == True \
									and user_authenticate.is_staff==False\
									and user_authenticate.is_superuser == False:
				login(request,user_authenticate)
				token, created = Token.objects.get_or_create(user=user_authenticate)
				return Response({
					"success"		: 	True,
					"credential" 	: 	True
					})
			else:
				return Response({
					"success"		: 	False,
					"credential" 	: 	False,
					"message"		: 	"Please enter valid login credentials!!"
					})
		except Exception as e:
			return Response({
				"success"	: 	False, 
				"message"	: 	"Error happened!!", 
				"errors"	: 	str(e)
				})
