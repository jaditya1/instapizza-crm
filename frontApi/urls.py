from django.urls import path

from frontApi.LiveFeed.cruststeam import Crustflix
from frontApi.views import FeatureListing,LogoBanner
from frontApi.track_order import TrackOrder
from frontApi.order.order import OrderData
from frontApi.nearestOutlet.outlet import RestaurantMapView
from frontApi.configuration.config import ConfigView
from frontApi.configuration.feature import FeatureProductList
from frontApi.configuration.all_config import ConfigDataView
from frontApi.configuration.google_analytics import GoogleAnalytics
from frontApi.menu.category import CatListing
from frontApi.menu.product import FullProductList
from frontApi.menu.customization import CustomeMgmt
from frontApi.coupon.discounts import CouponcodeView

from frontApi.paymentsetting.payment_config import PaymentConfig
from frontApi.order.distance_check import DistanceCheck

from frontApi.posapi.pos_data import PosData
# from frontApi.posapi.pos_list import PosListData
# from frontApi.posapi.pos_retrieve import PosRetrieve
from frontApi.posapi.update_company import UpdateCompany
from frontApi.posapi.register_pos_customer import Register
from frontApi.posapi.customer_csv import Customercsv
from frontApi.posapi.boat import BoatData

from frontApi.LiveFeed.stream import OutletCam
from frontApi.LiveFeed.allOutlets import ALLOutlets


urlpatterns = [
	#API Endpoints for authentication
	# path('listing_data/feature_product/',FeatureProductList.as_view()),
	path('logobanner/',LogoBanner.as_view()),

	path('trackorder/',TrackOrder.as_view()),

	path('order/place/',OrderData.as_view()),

	path('distance/check/',DistanceCheck.as_view()),

	path('outlet/OutletDetail/',RestaurantMapView.as_view()),
	path('configuration/',ConfigView.as_view()),
	path('featureproduct/',FeatureProductList.as_view()),

	path('customer/cat_list/',CatListing.as_view()),
	path('customer/menu_list_filter/',FullProductList.as_view()),
	path('customer/customize_data/',CustomeMgmt.as_view()),
	
	path('Couponcode/',CouponcodeView.as_view()),

	# Payment Gateway Setting
	path('payment/setting/',PaymentConfig.as_view()),


	# config data company wise

	path('configuration/all/',ConfigDataView.as_view()),
	path('configuration/google/analytics/',GoogleAnalytics.as_view()),


	path('pos/alldata/',PosData.as_view()),

	path('pos/boat/',BoatData.as_view()),

	path('pos/update/company/',UpdateCompany.as_view()),
	path('pos/register/',Register.as_view()),
	path('pos/csv/',Customercsv.as_view()),

	path('outlet/stream/', OutletCam.as_view()),
	path('all/stream/listing/', ALLOutlets.as_view()),
	path('crustflix/listing/', Crustflix.as_view()),

	]
