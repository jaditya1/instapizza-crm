from django.urls import path
from CustomerApi.Api.Authorization.registration import CustomerRegistration, OtpVerificationemail
from CustomerApi.Api.Authorization.signin import CustomerSignin, CustomerSignout

urlpatterns = [
	#API Endpoints for authentication
	path('registration/',CustomerRegistration.as_view()),
	path('OtpVerificationemail/apiview/', OtpVerificationemail.as_view()),
	path('signin/apiview/', CustomerSignin.as_view()),
	path('signout/apiview/', CustomerSignout.as_view())

]