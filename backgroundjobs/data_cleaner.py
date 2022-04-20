from Product.models import ProductCategory, ProductsubCategory, Variant,\
	AddonDetails, Addons, Product, FeatureProduct, Product_availability, Category_availability, \
	Tag
from django.db.models import Q
from Brands.models import Company
from Outlet.models import OutletProfile, OutletMilesRules, DeliveryBoy

from kitchen.models import Ingredient, StepToprocess, ProcessTrack

from Customers.models import CustomerProfile, customer_otp

from urbanpiper.models import OutletSync, OrderRawApiResponse, UrbanOrders 

from datetime import datetime, timedelta

def alldata_cleaner():
	now = datetime.now()
	today = now.date()
	time_24_hours_ago = now - timedelta(days=1, hours=5)
	# product_cleaner = Product.objects.\
	# filter(Q(Company=4)|Q(Company=3)|Q(Company=2)).delete()
	# featured_product_cleaner = \
	# FeatureProduct.objects.\
	# filter(Q(company=4)|Q(company=3)|Q(company=2)).delete()
	# tag_cleaner = \
	# Tag.objects.\
	# filter(Q(company=4)|Q(company=3)|Q(company=2)).delete()
	# product_availability_cleaner = Product_availability.objects.\
	# filter(Q(outlet__Company=4)|Q(outlet__Company=3)|Q(outlet__Company=2)).delete()
	# cat_availability_cleaner = Category_availability.objects.\
	# filter(Q(outlet__Company=4)|Q(outlet__Company=3)|Q(outlet__Company=2)).delete()
	# addons_cleaner = \
	# Addons.objects.\
	# filter(Q(Company=4)|Q(Company=3)|Q(Company=2)).delete()
	# addons_grp_cleaner = \
	# AddonDetails.objects.\
	# filter(Q(Company=4)|Q(Company=3)|Q(Company=2)).delete()
	# Variant_cleaner = \
	# Variant.objects.filter(Q(Company=4)|Q(Company=3)|Q(Company=2)).delete()
	# subcat_cleaner = \
	# ProductsubCategory.objects.\
	# filter(Q(category__Company=4)|Q(category__Company=3)|Q(category__Company=2)).delete()
	# cat_cleaner = \
	# ProductCategory.objects.filter(Q(Company=4)|Q(Company=3)|Q(Company=2)).delete()

	# DeliveryBoy_cleaner = \
	# DeliveryBoy.objects.filter(Q(Company=4)|Q(Company=3)|Q(Company=2)).delete()
	# milerules_cleaner = \
	# OutletMilesRules.objects.filter(Q(Company=4)|Q(Company=3)|Q(Company=2)).delete()

	# ProcessTrack_cleaner = ProcessTrack.objects.\
	# filter(Q(company=4)|Q(company=3)|Q(company=2)).delete()
	# StepToprocess_cleaner = \
	# StepToprocess.objects.\
	# filter(Q(company=4)|Q(company=3)|Q(company=2)).delete()
	# Ingredient_cleaner = \
	# Ingredient.objects.\
	# filter(Q(company=4)|Q(company=3)|Q(company=2)).delete()
	# Customers_cleaner = \
	# CustomerProfile.objects.\
	# filter(Q(company=4)|Q(company=3)|Q(company=2)).delete()
	UrbanOrders.objects.filter(created_at__lte=time_24_hours_ago).delete()
	print("done")