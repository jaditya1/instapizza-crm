from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Brands.models import Company
from Product.models import Product,Variant, ProductCategory
from django.db.models import Sum,Count
from kitchen.models import StepToprocess
from UserRole.models import ManagerProfile


class StepprocessList(APIView):

	"""
	Product process listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Product process.

	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request,format=None):
		try:
			user = self.request.user.id
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



			record = \
			StepToprocess.objects.filter(company__auth_user=nuser).\
			values('product','varient','product__product_name','varient__variant',\
				'product__product_category')\
			.annotate(total_time=Sum('time_of_process'),total_steps=Count('id'))
			final_result = []
			if record.count()!=0:
				for i in record:
					final_dict = {}
					final_dict["p_id"] = i["product"]
					final_dict["v_id"] = i["varient"]
					# final_dict["product"] = i["product__product_name"]
					final_dict["variant"] = i["varient__variant"]
					cat_name = \
					ProductCategory.objects.filter(id=i['product__product_category'])[0].category_name
					final_dict["product"] = i["product__product_name"] + " | " + cat_name
					final_dict["total_time"] = i["total_time"]
					final_dict["total_steps"] = i["total_steps"]
					final_dict["active_status"] = \
					StepToprocess.objects.filter(product=final_dict["p_id"],\
						varient=final_dict["v_id"])[0].active_status
					final_result.append(final_dict)
					# print(final_result)
			else:
				pass
			return Response({
						"success": True,
						"data" : final_result
						})
		except Exception as e:
			print("Product process listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})