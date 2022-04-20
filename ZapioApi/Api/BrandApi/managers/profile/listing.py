from rest_framework.views import APIView
from rest_framework.response import Response
from UserRole.models import ManagerProfile
from rest_framework.permissions import IsAuthenticated
from UserRole.models import ManagerProfile
from Brands.models import Company
class ManagersListing(APIView):
	"""
	Managers Profile listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of manager profile data within brand.
	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			user = request.user.id
			ch_brand = Company.objects.filter(auth_user_id=user)
			if ch_brand.count() > 0:
				nuser=user
			else:
				pass
			ch_cashier = ManagerProfile.objects.filter(auth_user_id=user)
			if ch_cashier.count() > 0:
				company_id = ch_cashier[0].Company_id
				auth_user_id = Company.objects.filter(id=company_id)[0].auth_user_id
				nuser=auth_user_id
			else:
				pass
			record = ManagerProfile.objects.filter(Company__auth_user=nuser).order_by('-created_at')
			final_result = []
			if record.count() > 0:
				for i in record:
					record_dict = {}
					record_dict['user_type'] = i.user_type.user_type
					record_dict['id'] = i.id
					record_dict['active_status'] = i.active_status
					record_dict['manager_name'] = i.manager_name
					email = i.email
					if email == None:
						record_dict['email'] = "N/A"
					else:
						record_dict['email'] = email
					record_dict['username'] = i.username
					record_dict['mobile'] = i.mobile
					
					final_result.append(record_dict)
				return Response({
						"success": True, 
						"data": final_result})
			else:
				return Response({
						"success": True, 
						"data": []})
		except Exception as e:
			print("ManagerProfile listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})