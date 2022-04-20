from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.sites.shortcuts import get_current_site

#Serializer for api
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from kitchen.models import Ingredient
from UserRole.models import ManagerProfile
from Brands.models import Company
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from zapio.settings import Media_Path



class IngredientlistingSerializer(serializers.ModelSerializer):
	food_name = serializers.ReadOnlyField(source='food_type.food_type')

	def to_representation(self, instance):
		representation = super(IngredientlistingSerializer, self).to_representation(instance)
		representation['created_at'] = instance.created_at.strftime("%d/%b/%y")
		domain_name = Media_Path
		representation['image'] = str(instance.image)
		if representation['image'] != "" and representation['image'] != None\
			and representation['image'] != "null":
			full_path = domain_name + str(instance.image)
			representation['image'] = full_path
		else:
			pass
		if instance.updated_at != None:
			representation['updated_at'] = instance.updated_at.strftime("%d/%b/%y")
		else:
			pass
		return representation

	class Meta:
		model = Ingredient
		fields = ['name','food_name','image','created_at','updated_at','active_status','id']


class IngredientList(ListAPIView):

	"""
	Ingredient listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Ingredients data.
	"""


	permission_classes = (IsAuthenticated,)
	def get_queryset(self):
		user = self.request.user.id
		Company_id = get_user(user)
		queryset = Ingredient.objects.filter(company=Company_id)
		return queryset

	def list(self, request):
		queryset = self.get_queryset()
		serializer = IngredientlistingSerializer(queryset, many=True)
		response_list = serializer.data 
		return Response({
					"success": True,
					"data" : response_list,
					"message" : "All Ingredients listing API worked well!!"})

