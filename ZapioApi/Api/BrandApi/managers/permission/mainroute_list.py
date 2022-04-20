from rest_framework.views import APIView
from rest_framework.response import Response
from UserRole.models import UserType, MainRoutingModule, RoutingModule, SubRoutingModule
from rest_framework.permissions import IsAuthenticated

class MainRouteListing(APIView):
	"""
	Main Route listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Main Routes.
	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			record = MainRoutingModule.objects.filter(active_status=1)
			final_result = []
			if record.count() > 0:
				for i in record:
					record_dict = {}
					record_dict['module_id'] = i.id
					record_dict['module_name'] = i.module_name
					final_result.append(record_dict)
				return Response({
						"success": True, 
						"data": final_result})
			else:
				return Response({
						"success": True, 
						"data": []})
		except Exception as e:
			print("Main Route listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})