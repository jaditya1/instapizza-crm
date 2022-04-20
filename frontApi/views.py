from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, \
	HTTP_406_NOT_ACCEPTABLE, HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.sites.shortcuts import get_current_site
from ZapioApi.Api.BrandApi.profile.profile import CompanySerializer
from Brands.models import Company

#Serializer for api
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from Product.models import FeatureProduct,Product
from zapio.settings import Media_Path

class FeatureListing(APIView):
	"""
	User listing GET API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for listing of User data within brand.
	"""
	# permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		url = request.data['wurl']
		company_data = Company.objects.filter(website=url).first()
		if company_data:
			featureData = FeatureProduct.objects.filter(company=company_data.id).first()
			feature_product_id = featureData.feature_product
			pro_data =[]
			for i in feature_product_id:
				p_list ={}
				product_data = Product.objects.filter(id=i).first()
				p_list['product_name'] = product_data.product_name
				p_list['product_code'] = product_data.product_code
				p_list['product_desc'] = product_data.product_desc
				if product_data.product_image != "" and product_data.product_image != None:
					full_path = Media_Path + str(product_data.product_image)
					p_list['product_image'] = full_path
				pro_data.append(p_list)
			return Response({"status":True,
							"data":pro_data})


class LogoBanner(APIView):
	"""
	User listing GET API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for listing of User data within brand.
	"""
	# permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		url = request.data['wurl']
		# url = "https://www.facebook.com"
		company_data = Company.objects.filter(website=url).first()
		p_list={}
		pdata = []
		# p_list['logo'] = company_data.company_logo
		# p_list['banner'] = company_data.company_landing_imge
		if company_data.company_logo != "" and company_data.company_logo != None:
			full_path = Media_Path + str(company_data.company_logo)
			p_list['logo'] = full_path
		if company_data.company_landing_imge != "" and company_data.company_landing_imge != None:
			full_path1 = Media_Path + str(company_data.company_landing_imge)
			p_list['banner'] = full_path1
		pdata.append(p_list)

		return Response({"status":True,
							"data":pdata})
