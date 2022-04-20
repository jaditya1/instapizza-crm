from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.sites.shortcuts import get_current_site
from ZapioApi.Api.BrandApi.profile.profile import CompanySerializer
from Brands.models import Company

#Serializer for api
from rest_framework import serializers
from Product.models import Variant, FoodType, AddonDetails, Product, ProductsubCategory,\
FeatureProduct,ProductCategory,ProductsubCategory
from rest_framework.authtoken.models import Token
from Location.models import CityMaster, AreaMaster
from UserRole.models import ManagerProfile
from Outlet.models import *
from urbanpiper.models import *
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from zapio.settings import Media_Path

class CompanySerializer(serializers.ModelSerializer):
	
	def to_representation(self, instance):
		representation = super(CompanySerializer, self).to_representation(instance)
		representation['created_at'] = instance.created_at.strftime("%d/%b/%y")
		domain_name = Media_Path
		representation['company_logo'] = str(instance.company_logo)
		if representation['company_logo'] != "" and representation['company_logo'] != None:
			full_path = domain_name + str(instance.company_logo)
			representation['company_logo'] = full_path
		else:
			pass
		representation['company_landing_imge'] = str(instance.company_landing_imge)
		if representation['company_landing_imge'] != "" and representation['company_landing_imge'] != None:
			full_path_banner = domain_name + str(instance.company_landing_imge)
			representation['company_landing_imge'] = full_path_banner
		else:
			pass			
		if instance.updated_at != None:
			representation['updated_at'] = instance.updated_at.strftime("%d/%b/%y")
		else:
			pass
		return representation

	class Meta:
		model = Company
		fields = '__all__'

class VariantlistingSerializer(serializers.ModelSerializer):
	# company_name = serializers.ReadOnlyField(source='Company.company_name')
	class Meta:
		model = Variant
		fields = '__all__'

class FoodTypelistingSerializer(serializers.ModelSerializer):

	def to_representation(self, instance):
		representation = super(FoodTypelistingSerializer, self).to_representation(instance)
		representation['created_at'] = instance.created_at.strftime("%d/%b/%y")
		domain_name = Media_Path
		representation['foodtype_image'] = str(instance.foodtype_image)
		if representation['foodtype_image'] != "" and representation['foodtype_image'] != None\
			and representation['foodtype_image'] != "null":
			full_path = domain_name + str(instance.foodtype_image)
			representation['foodtype_image'] = full_path
		else:
			pass
		if instance.updated_at != None:
			representation['updated_at'] = instance.updated_at.strftime("%d/%b/%y")
		else:
			pass
		return representation

	class Meta:
		model = FoodType
		fields = '__all__'

class AddonDetailslistingSerializer(serializers.ModelSerializer):
	variant_name = serializers.ReadOnlyField(source='product_variant.variant')

	def to_representation(self, instance):
		representation = super(AddonDetailslistingSerializer, self).to_representation(instance)
		if instance.product_variant != None:
			representation['addon_gr_name'] = \
			str(instance.addon_gr_name)+' | '+str(instance.product_variant.variant)
		else:
			pass
		if instance.description != None:
			representation['addon_gr_name'] = \
			representation['addon_gr_name']+'('+instance.description+')'
		else:
			pass
		return representation

	class Meta:
		model = AddonDetails
		fields = ['id','addon_gr_name','variant_name','min_addons','max_addons','active_status','description',\
					'addon_grp_type']

class CitylistingSerializer(serializers.ModelSerializer):
	class Meta:
		model = CityMaster
		fields = ['id','city']

class AreaMasterlslistingSerializer(serializers.ModelSerializer):
	class Meta:
		model = AreaMaster
		fields = '__all__'

class ProductlistingSerializer(serializers.ModelSerializer):
	category_name = serializers.ReadOnlyField(source='product_category.category_name')
	subcategory_name = serializers.ReadOnlyField(source='product_subcategory.subcategory_name')
	FoodType_name = serializers.ReadOnlyField(source='food_type.food_type')


	def to_representation(self, instance):
		representation = super(ProductlistingSerializer, self).to_representation(instance)
		representation['created_at'] = instance.created_at.strftime("%d/%b/%y")
		domain_name = Media_Path
		representation['product_image'] = str(instance.product_image)
		if representation['product_image'] != "" and representation['product_image'] != None\
			and representation['product_image'] != "null":
			full_path = domain_name + str(instance.product_image)
			representation['product_image'] = full_path
		else:
			pass
		if instance.updated_at != None:
			representation['updated_at'] = instance.updated_at.strftime("%d/%b/%y")
		else:
			pass
		return representation


	class Meta:
		model = Product
		fields = ['id','category_name','subcategory_name','FoodType_name','priority','product_code',\
				'product_name','product_desc','product_image','active_status','created_at','updated_at']

class ProductsubCategorySerializer(serializers.ModelSerializer):
	category_name = serializers.ReadOnlyField(source='category.category_name')

	def to_representation(self, instance):
		representation = super(ProductsubCategorySerializer, self).to_representation(instance)
		representation['created_at'] = instance.created_at.strftime("%d/%b/%y")
		if instance.updated_at != None:
			representation['updated_at'] = instance.updated_at.strftime("%d/%b/%y")
		else:
			pass
		return representation

	class Meta:
		model = ProductsubCategory
		fields = ['id','category_name','subcategory_name','active_status','created_at','updated_at']

def site_addr(request):
	current_site = get_current_site(request)
	domain = current_site.domain
	return domain


class Variantlisting(ListAPIView):
	"""
	Variant listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Variant data within brand.
	"""
	permission_classes = (IsAuthenticated,)
	serializer_class = VariantlistingSerializer

	def get_queryset(self):
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
		queryset = Variant.objects.all().order_by('-created_at')
		return queryset.filter(Company__auth_user=nuser)


class FoodTypelisting(ListAPIView):
	"""
	FoodType listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of FoodType data.
	"""
	permission_classes = (IsAuthenticated,)
	queryset = FoodType.objects.all().order_by('-created_at')
	serializer_class = FoodTypelistingSerializer







class AddonDetailslisting(APIView):
	"""
	AddonDetails POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide AddonDetails.

		Data Post: {

			"status"   ; "true"
		}

		Response: {

			"success": True,
			"data" : AddonDetails_data_serializer,
			"message": "Addon detail successful!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			user = request.user.id
			is_outlet = OutletProfile.objects.filter(auth_user_id=user)
			is_brand = Company.objects.filter(auth_user_id=user)
			is_cashier = ManagerProfile.objects.filter(auth_user_id=user)
			if is_cashier.count() > 0:
				cid = ManagerProfile.objects.filter(auth_user_id=user)[0].Company_id
			else:
				pass
			if is_outlet.count() > 0:
				outlet = OutletProfile.objects.filter(auth_user_id=user)
				cid = outlet[0].Company_id
			else:
				pass
			if is_brand.count() > 0:
				outlet = Company.objects.filter(auth_user_id=user)
				cid = outlet[0].id
			else:
				pass
			if data['status'] == True:
				query = AddonDetails.objects.\
						filter(Company_id=cid,active_status=1).order_by('-created_at')
			else:
				query = AddonDetails.objects.\
						filter(Company_id=cid,active_status=0).order_by('-created_at')

			result = []
			for q in query:
				q_dict = {}
				q_dict["id"] = q.id
				q_dict["description"] = q.description 
				q_dict["active_status"] = q.active_status
				q_dict["max_addons"] = q.max_addons
				q_dict["min_addons"] = q.min_addons
				q_dict["priority"] = q.priority
				q_dict["addon_grp_type"] = q.addon_grp_type
				a = q.product_variant_id
				if a != None:
					q_dict["variant_name"] = q.product_variant.variant
				else:
					q_dict["variant_name"] = None
				if q_dict["variant_name"] != None:
					q_dict["addon_gr_name"] = q.addon_gr_name+" | "+q_dict["variant_name"]
				else:
					q_dict["addon_gr_name"] = q.addon_gr_name
				result.append(q_dict)
			return Response(
					{
						"success": True,
						"data" : result,
	 					"message": "Addon details fetching successful!!"
					}
					)
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})

			
class Citylisting(ListAPIView):
	"""
	City listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Cities.
	"""
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		queryset = CityMaster.objects.filter(active_status=1)
		return queryset

	def list(self, request):
		queryset = self.get_queryset()
		serializer = CitylistingSerializer(queryset, many=True)
		response_list = serializer.data 
		return Response({
					"success": True,
					"data" : response_list,
					"message" : "City listing API worked well!!"})

class Productlisting(APIView):
	"""
	Product Listing POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide product Listing.

		Data Post: {

			"status"   ; "true"
		}

		Response: {

		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			user = request.user.id
			is_outlet = OutletProfile.objects.filter(auth_user_id=user)
			is_brand = Company.objects.filter(auth_user_id=user)
			is_cashier = ManagerProfile.objects.filter(auth_user_id=user)
			if is_cashier.count() > 0:
				cid = ManagerProfile.objects.filter(auth_user_id=user)[0].Company_id
			else:
				pass
			if is_outlet.count() > 0:
				outlet = OutletProfile.objects.filter(auth_user_id=user)
				cid = outlet[0].Company_id
			else:
				pass
			if is_brand.count() > 0:
				outlet = Company.objects.filter(auth_user_id=user)
				cid = outlet[0].id
			else:
				pass
			if data['status'] == True:
				query = Product.objects.\
						filter(Company_id=cid,active_status=1).order_by('-created_at')
			else:
				query = Product.objects.\
						filter(Company_id=cid,active_status=0).order_by('-created_at')

			catagory_conf_data_serializer = []
			for q in query:
				q_dict = {}
				q_dict["id"] = q.id
				sp = ProductSync.objects.filter(product_id = q.id)
				if sp.count() > 0:
					q_dict["ids"] = sp[0].id
				else:
					pass
				c = ProductCategory.objects.filter(id=q.product_category_id)
				if c.count() > 0:
					q_dict["category_name"] = c[0].category_name
				else:
					pass
				s = ProductsubCategory.objects.filter(id=q.product_subcategory_id)
				if s.count() > 0:
					q_dict["subcategory_name"] = s[0].subcategory_name
				else:
					pass
				f = FoodType.objects.filter(id=q.food_type_id)
				q_dict["FoodType_name"] = f[0].food_type
				q_dict["priority"] = q.priority
				q_dict["product_code"] = q.product_code
				q_dict["product_name"] = q.product_name
				q_dict["product_desc"] = q.product_desc 
				q_dict['created_at'] = q.created_at.strftime("%d/%b/%y")
				domain_name = Media_Path
				q_dict['product_image'] = str(q.product_image)
				if q_dict['product_image'] != "" and q_dict['product_image'] != None\
					and q_dict['product_image'] != "null":
					full_path = domain_name + str(q.product_image)
					q_dict['product_image'] = full_path
				else:
					pass
				if q.updated_at != None:
					q_dict['updated_at'] = q.updated_at.strftime("%d/%b/%y")
				q_dict["active_status"] = q.active_status
				catagory_conf_data_serializer.append(q_dict)
			return Response(
					{
						"success": True,
						"data" : catagory_conf_data_serializer,
	 					"message": "Addon details fetching successful!!"
					}
					)
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})





class SubCategorylisting(ListAPIView):
	"""
	Sub-Category listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Sub-Category.
	"""
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user
		user = user.id
		cid = get_user(user)
		queryset = \
		ProductsubCategory.objects.filter(category__Company=cid).order_by('-created_at')
		return queryset
	def list(self, request):
		queryset = self.get_queryset()
		serializer = ProductsubCategorySerializer(queryset, many=True)
		response_list = serializer.data 
		return Response({
					"success": True,
					"data" : response_list,
					"message" : "Sub-Category listing API worked well!!"})


class Companylisting(ListAPIView):
	"""
	Company detail listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for providing the profile details of brand.
	"""
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user
		auth_id = user.id
		Company_id = get_user(auth_id)
		queryset = Company.objects.filter(active_status=1, id=Company_id)
		return queryset

	def list(self, request):
		queryset = self.get_queryset()
		serializer = CompanySerializer(queryset, many=True)
		response_list = serializer.data 
		return Response({
					"success": True,
					"data" : response_list,
					"message" : "Company profile detail API worked well!!"})



class FeatureListing(APIView):
	"""
	User listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of featured product data within brand.
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
			record = FeatureProduct.objects.filter(company__auth_user=nuser)
			final_result = []
			if record.count() > 0:
				for i in record:
					feature_dict = {}
					feature_dict['outlet'] = i.outlet.Outletname
					feature_dict['id'] = i.id
					featured = i.feature_product
					featured_list = []
					if len(featured) != 0:
						for j in featured:
							q = Product.objects.filter(id=j,active_status=1)
							featured_list\
							.append(q[0].product_name+" | "+q[0].product_category.category_name)
					else:
						feature_dict["featured"] = None
					if len(featured_list) != 0:
						feature_dict["featured"] = \
						', '.join([str(elem) for elem in featured_list])
					else:
						feature_dict["featured"] = None
					feature_dict['active_status'] = i.active_status
					final_result.append(feature_dict)
				return Response({
						"success": True, 
						"data": final_result})
			else:
				return Response({
						"success": True, 
						"data": []})
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})





