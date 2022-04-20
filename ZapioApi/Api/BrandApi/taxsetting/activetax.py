from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Configuration.models import TaxSetting
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user



class ActiveTaxlisting(APIView):
	"""
	Active Tax listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of active Taxes brandwise.
	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			user = request.user.id
			cid = get_user(user)
			record = TaxSetting.objects.filter(active_status=1,company=cid)
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Required data is not found!!"
				}
				)
			else:
				final_result = []
				for q in record:
					q_dict = {}
					q_dict["id"] =  q.id
					q_dict["tax_name"] = \
					str(q.tax_name)+" | "+str(q.tax_percent)+"%" 
					final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "Active tax data listing api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Active tax data listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})