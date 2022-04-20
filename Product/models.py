from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum
# from configuration.models import *
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.safestring import mark_safe
from zapio.settings import MEDIA_URL
# from outletmanager.models import InstaOutletProfile
from Brands.models import Company
from django.contrib.postgres.fields import ArrayField,JSONField
from Outlet.models import OutletProfile

# Create your models here.



class ProductCategory(models.Model):
	category_name = models.CharField(max_length=50, verbose_name='Category Name')
	category_code = models.CharField(max_length=20, verbose_name='Category Code',
																	 null=True,
																	blank=True,)
	Company = models.ForeignKey(Company, related_name='category_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	outlet_map = ArrayField(models.TextField(),null=True, blank=True, verbose_name="Outlet Mapped Ids")
	description = models.CharField(max_length=200, null=True, 
										blank=True, verbose_name='Description')
	priority = models.PositiveIntegerField(null=True, blank=True, verbose_name='Priority')
	active_status = models.BooleanField(default=1, verbose_name='Is Active')
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																		'Updation Date & Time')

	class Meta:
			verbose_name = 'Category'
			verbose_name_plural = '             Categories'
			unique_together = ('category_name','Company')

	def __str__(self):
			if self.category_name:
					return self.category_name

class ProductsubCategory(models.Model):
	category = models.ForeignKey(ProductCategory, related_name='Products_subcategory',
												on_delete=models.CASCADE,verbose_name='Category Name',
												limit_choices_to={'active_status':'1'})
	subcategory_name = models.CharField(max_length=50, verbose_name='Subcategory Name')
	active_status = models.BooleanField(default=1, verbose_name='Is Active')
	priority = models.PositiveIntegerField(null=True, blank=True, verbose_name='Priority')
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																		'Updation Date & Time')

	class Meta:
			verbose_name = '   Sub-Category'
			verbose_name_plural = '             Sub-Categories'

	def __str__(self):
			if self.subcategory_name:
					return self.subcategory_name


class FoodType(models.Model):
	food_type =  models.CharField(max_length=50, verbose_name='Food Type Name',
																	 unique=True)
	foodtype_image = \
			models.ImageField(upload_to='foodtype_images/images',
								verbose_name='Image (Short image)',blank=True, null=True,)
	active_status = models.BooleanField(default=1, verbose_name='Is Active')
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																		'Updation Date & Time')

	class Meta:
			verbose_name = 'Food Type'
			verbose_name_plural = '            Food Type'

	def __str__(self):
			return self.food_type

	def food_type_pic(self):
			if self.foodtype_image:
					return mark_safe('<img src='+MEDIA_URL+'%s width="25" height="25" />' %
											(self.foodtype_image))
					logo.allow_tags = True
			else:
					return 'No Image'
	food_type_pic.short_description = 'Food Type Image'


class Variant(models.Model):
	variant =  models.CharField(max_length=130, verbose_name="Variant Measurement")
	description =  models.CharField(max_length=110, null=True, blank=True,verbose_name="Description")
	Company = models.ForeignKey(Company, related_name='Variant_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	active_status = models.BooleanField(default=1, verbose_name='Is Active')
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																		'Updation Date & Time')

	def __str__(self):
			return self.variant

	class Meta:
			verbose_name = 'Variant'
			verbose_name_plural = '          Variants'


class AddonDetails(models.Model):
	addon_gr_name = models.CharField(max_length=50, verbose_name='Addon Group Name')
	min_addons = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)], 
		verbose_name='Minimum No. of Add-Ons', null=True, blank=True)
	max_addons = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(100)], 
		verbose_name='Maximum No. of Add-Ons', null=True, blank=True)
	product_variant = models.ForeignKey(Variant,on_delete=models.CASCADE,
												verbose_name='Variant',
												limit_choices_to={'active_status':'1'},
												null=True, blank=True)
	Company = models.ForeignKey(Company, related_name='Addon_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	description = models.CharField(max_length=200, blank=True, verbose_name='Description')
	priority = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(10000),], 
						verbose_name='Priority', null=True, blank=True, unique=True)
	associated_addons = JSONField(blank=True,null=True)
	is_crust = models.BooleanField(default=0,verbose_name="Is Crust")
	is_zomato_crust = models.BooleanField(default=0,verbose_name="Is Zomato Crust")
	zomato_nested_crusts = \
	ArrayField(models.TextField(),null=True, blank=True, verbose_name="Mapped Nested Group Ids")
	addon_grp_type = models.CharField(max_length=50, choices=[
						('0','Is Crust'), 
						('1','Is Sauce'),
						('2','Is Cheese'),
						('3','Is Base Topping'),
						('4', 'Is Normal Topping')
							], verbose_name='Addon Group Type',null=True,blank=True)
	active_status = models.BooleanField(default=1,null=True,blank=True,verbose_name="Is Active")
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(blank=True, null=True,verbose_name='Updation Date')

	def __str__(self):
		if self.product_variant != None:
			return self.addon_gr_name+' | '+self.product_variant.variant
		else:
			return self.addon_gr_name

	class Meta:
			verbose_name = 'Add-on Group'
			verbose_name_plural = '         Add-on Groups'


class Addons(models.Model):
	Company = models.ForeignKey(Company, related_name='Addons_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	name = models.CharField(max_length=250, verbose_name='Add-On Name')
	identifier = models.CharField(max_length=250,blank=True,null=True, verbose_name='Add on Identifier')

	addon_amount = models.FloatField(blank=True,null=True,verbose_name='Add-On Amount')
	addon_group = models.ForeignKey(AddonDetails, related_name='addon_gouping',
												on_delete=models.CASCADE,verbose_name='Add-On Group',
									limit_choices_to={'active_status':'1'}, null=True, blank=True)
	priority = models.PositiveIntegerField(null=True, blank=True, verbose_name='Priority')
	active_status = models.BooleanField(default=1, verbose_name='Is Active')
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
														'Updation Date & Time')

	class Meta:
			verbose_name = 'Add-on'
			verbose_name_plural = '         Add-ons'

	def __str__(self):
			if self.name:
					return self.name


class Product(models.Model):
	product_category = models.ForeignKey(ProductCategory, related_name='Product_Category',
													on_delete=models.CASCADE,verbose_name='Product Category',
														limit_choices_to={'active_status':'1'})

	product_subcategory = models.ForeignKey(ProductsubCategory, related_name='Product_subCategory',
													on_delete=models.CASCADE,verbose_name='Product Sub Category',
													limit_choices_to={'active_status':'1'},
													blank=True,null=True)
	product_name = models.CharField(max_length=100, verbose_name='Product Name')
	food_type = models.ForeignKey(FoodType,on_delete=models.CASCADE,
																verbose_name='Product Type',
																limit_choices_to={'active_status':'1'})
	priority = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(10000),], 
						verbose_name='Priority', null=True, blank=True)
	Company = models.ForeignKey(Company, related_name='Product_Company',
							on_delete=models.CASCADE,verbose_name='Company',
							limit_choices_to={'active_status':'1'},null=True, blank=True)
	product_code = models.CharField(max_length=20, verbose_name='Product Code',
																	 null=True, blank=True)
	product_desc = models.TextField(verbose_name='Product Description',
																	 null=True, blank=True)

	kot_desc = models.CharField(max_length=200, verbose_name='Kot Description',
																	 null=True, blank=True)

	product_image =  models.ImageField(upload_to='product_image/', verbose_name='Image', 
																null=True,blank=True)
	tags = ArrayField(models.TextField(),blank=True,null=True, verbose_name="Mapped Tag Ids")
	has_variant = models.BooleanField(default=1, verbose_name='Has Variant')
	price = models.FloatField(blank=True,null=True,verbose_name='Product Price')
	discount_price = models.FloatField(blank=True,null=True,verbose_name='Discount Product Price')
	variant_deatils = JSONField(blank=True,null=True)
	addpn_grp_association = ArrayField(models.TextField(), blank=True,null=True)
	tax_association = ArrayField(models.TextField(), blank=True,null=True, verbose_name="Tax Ids")
	outlet_map = ArrayField(models.TextField(),blank=True,null=True, verbose_name="Outlet Mapped Ids")
	active_status = models.BooleanField(default=1, verbose_name='Is Active')
	is_recommended = \
	models.BooleanField(default=True, verbose_name='Is Recommended')
	included_platform = ArrayField(models.TextField(),null=True, blank=True,\
			 verbose_name="Included Plateform")
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																		'Updation Date & Time')


	def image(self):
			if self.product_image:
					return mark_safe('<img src='+MEDIA_URL+'%s width="50" height="50" />' % (self.product_image))
			return 'No Image'
	image.short_description = 'Product Image'

	class Meta:
			verbose_name = 'Product'
			verbose_name_plural = '       Products'

	def __str__(self):
			return self.product_name+' | '+self.food_type.food_type


class FeatureProduct(models.Model):
	company = models.ForeignKey(Company, related_name='FeatureProduct_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	feature_product = ArrayField(models.TextField(), blank=True, null=True,verbose_name="Feature_product ID")
	active_status = models.BooleanField(default=1, verbose_name='Is Active')
	outlet = models.ForeignKey(OutletProfile,on_delete=models.CASCADE,verbose_name='Outlet',
												limit_choices_to={'active_status':'1'},
												blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																		'Updation Date & Time')

	def _str_(self):
			return str(self.Company)

	class Meta:
			verbose_name = 'Feature'
			verbose_name_plural = '          Feature Product'


class Product_availability(models.Model):
	outlet = models.ForeignKey(OutletProfile,on_delete=models.CASCADE,verbose_name='Outlet',
												limit_choices_to={'active_status':'1'},
												blank=True, null=True)
	available_product = ArrayField(models.TextField(),null=True, blank=True, verbose_name="Available_product ID")
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																		'Updation Date & Time')


class Category_availability(models.Model):
	outlet = models.ForeignKey(OutletProfile,on_delete=models.CASCADE,verbose_name='Outlet',
												limit_choices_to={'active_status':'1'},
												blank=True, null=True)
	available_cat = ArrayField(models.TextField(),null=True, blank=True, verbose_name="Available_category ID")
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(null=True, blank=True, verbose_name=
																		'Updation Date & Time')



class Tag(models.Model):
	company = models.ForeignKey(Company, related_name='Tag_Company',
									on_delete=models.CASCADE,verbose_name='Company',
									limit_choices_to={'active_status':'1'})
	tag_name = models.CharField(max_length=100,blank=True, null=True, verbose_name='Tag Name')
	tag_image =  models.ImageField(upload_to='tag_image/', verbose_name='Image', 
																null=True,blank=True)
	food_type = models.ForeignKey(FoodType, related_name='Tag_food',
										on_delete=models.CASCADE,verbose_name='Food Type',
										limit_choices_to={'active_status':'1'},blank=True, null=True)
	active_status = models.BooleanField(default=0, verbose_name='Is Active')
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(blank=True, null=True,verbose_name='Updation Date & Time')
	
	class Meta:
		verbose_name = ' Tag'
		verbose_name_plural = ' Tag'

	def __str__(self):
		return self.tag_name


class KotSteps(models.Model):
	Company = models.ForeignKey(Company, related_name='KotSteps_Company',
							on_delete=models.CASCADE,verbose_name='Company',
							limit_choices_to={'active_status':'1'})
	product = models.ForeignKey(Product, related_name='KotSteps_Product',
							on_delete=models.CASCADE,verbose_name='Product',
							limit_choices_to={'active_status':'1'})
	variant = models.ForeignKey(Variant, related_name='KotSteps_variant',
							on_delete=models.CASCADE,verbose_name='Variant',
							limit_choices_to={'active_status':'1'},null=True,blank=True)
	kot_category = models.CharField(max_length=50, choices=[
						('0','Make Line'), 
						('1','Cut Table'),
							], verbose_name='KOT Catefory Type',null=True,blank=True)
	step_name = models.CharField(max_length=50, choices=[
						('0','Description'), 
						('1','Crust'),
						('2','Base Sauce'), 
						('3','Toppings'), 
						('4','Additional Toppings'),
						('5','Cheese'), 
						('6','Extra Cheese'),
						('7','Sauce on Top'),
						('8','Garnishes'), 
						('9','Add-ons'),
						('10','Fried Filling'),
						('11','Seasoning')
							], verbose_name='Step Name',null=True,blank=True)

	kot_desc = models.TextField(verbose_name='KOT Description',null=True, blank=True)
	active_status = models.BooleanField(default=1, verbose_name='Is Active')
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(blank=True, null=True,verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = ' Item KOT Description'
		verbose_name_plural = ' Item KOT Description'

	def __str__(self):
		return str(self.product)


class ProductApiLog(models.Model):
	request_data = JSONField(blank=True,null=True, verbose_name="Request Data")
	request_file = models.FileField(upload_to='APILogFile/',blank=True,null=True,verbose_name="Request File",)
	response_data = JSONField(blank=True,null=True, verbose_name="Response Data")
	created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date & Time')

	class Meta:
		verbose_name = ' Product Api Log'
		verbose_name_plural = ' Product Api Log'

	def __str__(self):
		return str(self.request_data)



class CachedMenuData(models.Model):
	outlet = models.ForeignKey(OutletProfile,on_delete=models.CASCADE,
												verbose_name='Outlet',
												limit_choices_to={'active_status':'1'},
												null=True, blank=True)
	menu_data = JSONField(blank=True,null=True,verbose_name='Menu Data')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(blank=True, null=True,verbose_name='Updation Date')

	def __str__(self):
		return str(self.outlet)

	class Meta:
			verbose_name = 'Cached Menu Data'
			verbose_name_plural = 'Cached Menu Data'

