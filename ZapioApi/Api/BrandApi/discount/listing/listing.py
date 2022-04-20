from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.sites.shortcuts import get_current_site
from ZapioApi.Api.BrandApi.profile.profile import CompanySerializer
from Brands.models import Company

#Serializer for api
from rest_framework import serializers
from discount.models import Coupon, QuantityCombo, PercentCombo
from rest_framework.authtoken.models import Token
from UserRole.models import ManagerProfile
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

class CouponSerializer(serializers.ModelSerializer):
	category_name = serializers.ReadOnlyField(source = 'category.category_name')

	def to_representation(self, instance):
		representation = super(CouponSerializer, self).to_representation(instance)
		representation['created_at'] = instance.created_at.strftime("%d/%b/%y")
		representation['valid_frm'] = instance.valid_frm.strftime("%d/%b/%y")
		representation['valid_till'] = instance.valid_till.strftime("%d/%b/%y")

		if instance.updated_at != None:
			representation['updated_at'] = instance.updated_at.strftime("%d/%b/%y")
		else:
			pass
		return representation

	class Meta:
		model = Coupon
		fields = ['id','coupon_type','frequency','valid_frm','valid_till',\
					'category_name',\
		'flat_discount','flat_percentage','is_min_shop','is_automated','min_shoping',\
		'max_shoping','active_status','coupon_code']


class QuantityComboSerializer(serializers.ModelSerializer):
	product_name = serializers.ReadOnlyField(source = 'product.product_name')
	free_product_name = serializers.ReadOnlyField(source = 'free_product.product_name')

	def to_representation(self, instance):
		representation = super(QuantityComboSerializer, self).to_representation(instance)
		representation['created_at'] = instance.created_at.strftime("%d/%b/%y")
		representation['valid_frm'] = instance.valid_frm.strftime("%d/%b/%y")
		representation['valid_till'] = instance.valid_till.strftime("%d/%b/%y")

		if instance.updated_at != None:
			representation['updated_at'] = instance.updated_at.strftime("%d/%b/%y")
		else:
			pass
		return representation

	class Meta:
		model = QuantityCombo
		fields = ['id','combo_name', 'product_name','free_product_name','valid_till','valid_frm',\
		'product_quantity','free_pro_quantity','active_status']


class PercentComboSerializer(serializers.ModelSerializer):
	product_name = serializers.ReadOnlyField(source = 'product.product_name')
	discount_product_name = serializers.ReadOnlyField(source = 'discount_product.product_name')

	def to_representation(self, instance):
		representation = super(PercentComboSerializer, self).to_representation(instance)
		representation['created_at'] = instance.created_at.strftime("%d/%b/%y")
		representation['valid_frm'] = instance.valid_frm.strftime("%d/%b/%y")
		representation['valid_till'] = instance.valid_till.strftime("%d/%b/%y")

		if instance.updated_at != None:
			representation['updated_at'] = instance.updated_at.strftime("%d/%b/%y")
		else:
			pass
		return representation

	class Meta:
		model = PercentCombo
		fields = ['id', 'product_name','discount_product_name','valid_till','valid_frm',\
		'discount_percent','pcombo_name','active_status']


class Couponlisting1(ListAPIView):
	"""
	Coupon detail listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for providing the Coupon details of brand.
	"""
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user.id
		Company_id = get_user(user)
		queryset = Coupon.objects.filter(Company=Company_id).order_by('-created_at')
		return queryset

	def list(self, request):
		queryset = self.get_queryset()
		serializer = CouponSerializer(queryset, many=True)
		response_list = serializer.data 
		return Response({
					"success": True,
					"data" : response_list,
					"message" : "Coupon profile detail API worked well!!"})


class QuantityCombolisting(ListAPIView):
	"""
	Quantity Combo detail listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for providing the Quantity based Combo details of brand.
	"""
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user.id
		Company_id = get_user(user)
		queryset = QuantityCombo.objects.filter(Company=Company_id).order_by('-created_at')
		return queryset

	def list(self, request):
		queryset = self.get_queryset()
		serializer = QuantityComboSerializer(queryset, many=True)
		response_list = serializer.data 
		return Response({
					"success": True,
					"data" : response_list,
					"message" : "Quantity Combo detail API worked well!!"})



class PercentCombolisting(ListAPIView):
	"""
	Percent Combo detail listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for providing the Percent based Combo details of brand.
	"""
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user.id
		Company_id = get_user(user)
		queryset = PercentCombo.objects.filter(Company=Company_id).order_by('-created_at')
		return queryset

	def list(self, request):
		queryset = self.get_queryset()
		serializer = PercentComboSerializer(queryset, many=True)
		response_list = serializer.data 
		return Response({
					"success": True,
					"data" : response_list,
					"message" : "Percent Combo detail API worked well!!"})