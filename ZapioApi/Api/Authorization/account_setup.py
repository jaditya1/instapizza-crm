from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Brands.models import Company
from Configuration.models import ColorSetting, TaxSetting, PaymentDetails
from Outlet.models import OutletProfile, OutletMilesRules

class BrandSetupInfo(APIView):
	"""
	Brand configuration info GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide info about brand configuration set up.

	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			user = request.user.id
			is_brand = Company.objects.filter(auth_user_id=user)
			if is_brand.count() != 0:
				cid = is_brand[0].id
			else:
				return Response({
					"success" 	: 	False,
					"message"	:	"Configuration set up is not possible with this user type!!"
					})
			result = []
			brand_chk = is_brand[0]
			brand_dict = {}
			if brand_chk.company_logo != None and brand_chk.company_logo != "" and \
				brand_chk.company_landing_imge != None and brand_chk.company_landing_imge != ""\
				and brand_chk.support_person_email_id != None:
				brand_dict["is_set"] = True
			else:
				brand_dict["is_set"] = False
			brand_dict["content"] = "Basic account set up!!"
			result.append(brand_dict)
			tax_check = TaxSetting.objects.filter(company__auth_user=user)
			tax_dict = {}
			if tax_check.count() == 0:
				tax_dict["is_set"] = False
			else:
				if tax_check[0].tax_name != None and tax_check[0].tax_name != "" and \
					tax_check[0].tax_percent != None and tax_check[0].tax_percent != "":
					tax_dict["is_set"] = True
				else:
					tax_dict["is_set"] = False
			tax_dict["content"] = "Tax Configuration set up!!"
			result.append(tax_dict)
			pay_chk = PaymentDetails.objects.filter(company__auth_user=user,active_status=1)
			pay_dict = {}
			if pay_chk.count() == 0:
				pay_dict["is_set"] = False
			else:
				if pay_chk[0].keyid != None and pay_chk[0].keyid != "" and \
					pay_chk[0].keySecret != None and pay_chk[0].keySecret != "":
					pay_dict["is_set"] = True
				else:
					pay_dict["is_set"] = False
			pay_dict["content"] = "Payment gateway set up!!"
			result.append(pay_dict)
			outlet_check = OutletProfile.objects.filter(Company__auth_user=user,active_status=1)
			outlet_dict = {}
			outlet_dict["is_set"] = False
			for i in outlet_check:
				if i.opening_time != None and i.opening_time != "" and i.closing_time != None \
					and i.closing_time != "":
					outlet_dict["is_set"] = True
				else:
					outlet_dict["is_set"] = False
					break
			outlet_dict["content"] = "Outlet Timing set up!!"
			result.append(outlet_dict)
			service_rule_chk = OutletMilesRules.objects.filter(Company__auth_user=user,active_status=1)
			service_dict = {}
			if service_rule_chk.count() == 0:
				service_dict["is_set"] = False
			else:
				service_dict["is_set"] = True
			service_dict["content"] = "Brand delivery radious set up!!"
			result.append(service_dict)
			return Response(
					{
						"success"	: 	True,
						"data" 		: 	result,
						"message"	: 	"Api worked well!!"
					}
					)
		except Exception as e:
			print("Account Set Up Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})