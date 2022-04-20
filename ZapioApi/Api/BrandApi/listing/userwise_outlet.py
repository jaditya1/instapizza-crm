from rest_framework.views import APIView
from rest_framework.response import Response
from ZapioApi.Api.outlet_ids import outlets
from rest_framework.permissions import IsAuthenticated
from rest_framework_tracking.mixins import LoggingMixin


class UserOutlet(LoggingMixin,APIView):
	"""
	Outlet User WISE GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide User Wise Outlets.

	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			user_id = request.user.id
			outlet_list = outlets(user_id) 
			return Response(outlet_list)
		except Exception as e:
			print("User Wise Api Stucked into exception!!")
			print(e)
			return Response({"success": False, 
				"message": "Error happened!!", 
				"errors": str(e)})