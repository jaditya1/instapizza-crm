from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.sites.shortcuts import get_current_site
from ZapioApi.Api.BrandApi.profile.profile import CompanySerializer
from Brands.models import Company

#Serializer for api
from rest_framework import serializers
from discount.models import Coupon, QuantityCombo, PercentCombo,Discount
from rest_framework.authtoken.models import Token
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

class CouponSerializer(serializers.ModelSerializer):
	# category_name = serializers.ReadOnlyField(source = 'category.category_name')

	def to_representation(self, instance):
		representation = super(CouponSerializer, self).to_representation(instance)
		representation['created_at'] = instance.created_at.strftime("%d/%b/%y")
		if instance.valid_frm !=None:
			representation['valid_frm'] = instance.valid_frm.strftime("%d/%b/%y")
		else:
			pass
		if instance.valid_till !=None:
			representation['valid_till'] = instance.valid_till.strftime("%d/%b/%y")
		else:
			pass

		if instance.updated_at != None:
			representation['updated_at'] = instance.updated_at.strftime("%d/%b/%y")
		else:
			pass
		return representation

	class Meta:
		model = Discount
		fields = ['id',
				  'discount_type',
				  'discount_name',
				  'valid_frm',
				  'valid_till',
				  'active_status']


class Couponlisting(ListAPIView):
	"""
	Coupon detail listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for providing the Coupon details of brand.
	"""
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user
		auth_id = user.id
		Company_id = get_user(auth_id)
		queryset = Discount.objects.filter(Company=Company_id).order_by('-created_at')
		return queryset

	def list(self, request):
		queryset = self.get_queryset()
		serializer = CouponSerializer(queryset, many=True)
		response_list = serializer.data 
		return Response({
					"success": True,
					"data" : response_list,
					"message" : "Discount profile detail API worked well!!"})

