from django.urls import path, include
from ZapioApi.Api.BrandApi.outlet_creation import OutletCreation, OutletRetreive
from ZapioApi.Api.BrandApi.configuration_data import OutletListing, CatagoryListing, \
SubCatagoryListing,CatagoryWiseOutletListing, CatagoryWiseSubCategoryListing,\
CityWiseAreaListing

from ZapioApi.Api.BrandApi.cat_create_update import CategoryCreationUpdation
from ZapioApi.Api.BrandApi.subcat_create_update import SubCategoryCreation, SubCategoryUpdation
from ZapioApi.Api.BrandApi.foodtype_create_update import FoodTypeCreationUpdation
from ZapioApi.Api.BrandApi.variant_create_update import VariantCreationUpdation
from ZapioApi.Api.BrandApi.addon_create_update import AddonCreationUpdation, AddonAssociateCreationUpdation
from ZapioApi.Api.BrandApi.product_create_update import ProductCreationUpdation

from ZapioApi.Api.BrandApi.retrieve.category import CategoryRetrieval
from ZapioApi.Api.BrandApi.retrieve.subcategory import SubCategoryRetrieval
from ZapioApi.Api.BrandApi.retrieve.variant import VariantRetrieval
from ZapioApi.Api.BrandApi.retrieve.foodtype import FoodTypeRetrieval
from ZapioApi.Api.BrandApi.retrieve.AddonDetails import AddonDetailsRetrieval
from ZapioApi.Api.BrandApi.retrieve.product import ProductRetrieval
from ZapioApi.Api.BrandApi.retrieve.feature import FeatureRetrieval

from ZapioApi.Api.BrandApi.listing.listing import Variantlisting, AddonDetailslisting,\
FoodTypelisting, Citylisting, Productlisting,SubCategorylisting, Companylisting, FeatureListing

from ZapioApi.Api.BrandApi.listing.activelisting import VariantActive, FoodTypeActive,\
CategoryActive,AddonDetailsActive,Outletlisting,ActiveProductlisting,ActiveIngredient


from ZapioApi.Api.BrandApi.listing.userwise_outlet import UserOutlet


from ZapioApi.Api.BrandApi.action.product import ProductAction
from ZapioApi.Api.BrandApi.action.category import CategoryAction
from ZapioApi.Api.BrandApi.action.subcategory import SubCategoryAction
from ZapioApi.Api.BrandApi.action.variant import VariantAction
from ZapioApi.Api.BrandApi.action.AddonDetails import AddonDetailsAction
from ZapioApi.Api.BrandApi.action.foodtype import FoodTypeAction
from ZapioApi.Api.BrandApi.action.outlet import OutletAction
from ZapioApi.Api.BrandApi.action.feature import FeatureAction

from ZapioApi.Api.BrandApi.productdata.product import ProductListFilter
from ZapioApi.Api.BrandApi.productdata.taglist import ActiveTagList
from ZapioApi.Api.BrandApi.productdata.multiple_category_product import MultipleCategoryFilter
from ZapioApi.Api.BrandApi.productdata.product_level_report import ProductLevelReport
from ZapioApi.Api.BrandApi.productdata.product_level_csv import ProductLevelCSV

from ZapioApi.Api.BrandApi.profile.profile import ProfileUpdation

from ZapioApi.Api.BrandApi.discount.coupon_create_update import CouponCreationUpdation1
from ZapioApi.Api.BrandApi.discount.combo_create_update import QuantityComboCreationUpdation,\
PercentComboCreationUpdation
from ZapioApi.Api.BrandApi.discount.listing.listing import Couponlisting1, QuantityCombolisting,\
PercentCombolisting
from ZapioApi.Api.BrandApi.discount.retrieve.coupon import CouponRetrieval1
from ZapioApi.Api.BrandApi.discount.retrieve.combo import QuantityComboRetrieval,\
PercentComboRetrieval
from ZapioApi.Api.BrandApi.discount.action.coupon import CouponAction
from ZapioApi.Api.BrandApi.discount.action.Combo import QuantityComboAction,\
PercentComboAction

from ZapioApi.Api.Authorization.auth import BrandOutletlogin, BrandOutletlogout,\
IposOTPVerify
from ZapioApi.Api.Authorization.change_pwd import ChangePassword
from ZapioApi.Api.Authorization.account_setup import BrandSetupInfo

from ZapioApi.Api.BrandApi.feature_product_create_update import Feature

from ZapioApi.Api.BrandApi.order.listing import Orderlisting

from ZapioApi.Api.BrandApi.addons.addon import AssociateAddon

from ZapioApi.Api.BrandApi.outletmgmt.outletwiselisting.category import OutletCategorylist
from ZapioApi.Api.BrandApi.outletmgmt.outletwiselisting.product import OutletProductlist
from ZapioApi.Api.BrandApi.outletmgmt.listing.outlet import OutletIdNamelisting
from ZapioApi.Api.BrandApi.outletmgmt.availability.category import BrandLevelCategory
from ZapioApi.Api.BrandApi.outletmgmt.availability.product import BrandLevelProductavail
from ZapioApi.Api.BrandApi.outletmgmt.is_open import OutletIsOpen
from ZapioApi.Api.BrandApi.outletmgmt.timing import OutletTiming
from ZapioApi.Api.BrandApi.outletmgmt.retrieve import OutletTimeRetrieval

from ZapioApi.Api.BrandApi.ordermgmt.listing import OrderListingData
from ZapioApi.Api.BrandApi.ordermgmt.retrieve import BrandOrderRetrieval
from ZapioApi.Api.BrandApi.ordermgmt.change_status import ChangeStatusData

from ZapioApi.Api.BrandApi.sound.sound import SoundStatus, ChangeSound
from ZapioApi.Api.Dropbox.list_reports import  Dropboxlisting,Dropboxdeleting
# from ZapioApi.Api.DunzoApi.quote import UnprocessedQuote

from ZapioApi.push import PushHome

#  Kitchen
from ZapioApi.Api.BrandApi.kitchen.ingredient_create_update import IngredientCreationUpdation
from ZapioApi.Api.BrandApi.kitchen.ingredient_action import IngredientAction
from ZapioApi.Api.BrandApi.kitchen.ingredient_list import IngredientList
from ZapioApi.Api.BrandApi.kitchen.ingredient_retrieve import IngredientRetrieval
from ZapioApi.Api.BrandApi.kitchen.stepprocess import StepprocessCreateUpdate
from ZapioApi.Api.BrandApi.kitchen.process_list import StepprocessList
from ZapioApi.Api.BrandApi.kitchen.process_view import StepprocessView
from ZapioApi.Api.BrandApi.kitchen.retrieve import StepprocessRetrieve
from ZapioApi.Api.BrandApi.kitchen.status_process import ProcessAction
from ZapioApi.Api.BrandApi.kitchen.variant_list import ProductWiseVariant
from ZapioApi.Api.BrandApi.kitchen.step_delete import StepProcessDelete
from ZapioApi.Api.BrandApi.kitchen.step_bet import StepProcessBetween

from ZapioApi.Api.BrandApi.kitchen.remaining_step_data import StepProcessRemaining

# Notification
from ZapioApi.Api.BrandApi.notification.order_notification import (orderNotificationCount,
																	orderNotificationAll,
																	orderNotificationSeen)

# payment Configuration
from ZapioApi.Api.BrandApi.paymentsetting.payment_config import PaymentConfig
from ZapioApi.Api.BrandApi.paymentsetting.payment_edit import PaymentEdit
from ZapioApi.Api.BrandApi.paymentsetting.payment_retrieve import PaymentRetrieve
from ZapioApi.Api.BrandApi.paymentsetting.payment_action import PaymentAction

# Theme Configuration
from ZapioApi.Api.BrandApi.themesetting.theme_config import ThemeConfig
from ZapioApi.Api.BrandApi.themesetting.theme_edit import ThemeEdit
from ZapioApi.Api.BrandApi.themesetting.theme_retrieve import ThemeRetrieve
from ZapioApi.Api.BrandApi.themesetting.theme_action import ThemeAction

# Delivery Charge Configuration
from ZapioApi.Api.BrandApi.deliverysetting.delivery_config import DeliveryConfig
from ZapioApi.Api.BrandApi.deliverysetting.delivery_edit import DeliveryEdit
from ZapioApi.Api.BrandApi.deliverysetting.delivery_action import DeliveryAction

# Analytics Configuration
from ZapioApi.Api.BrandApi.analyticsSetting.analytics_config import AnalyticsConfig
from ZapioApi.Api.BrandApi.analyticsSetting.analytics_edit import AnalyticsEdit
from ZapioApi.Api.BrandApi.analyticsSetting.analytics_action import AnalyticsAction

# CustomerMgmt 
from ZapioApi.Api.BrandApi.CustomerMgmt.listing import  ActiveCustomer
from ZapioApi.Api.BrandApi.CustomerMgmt.customer_list import UserlistingSearch


from ZapioApi.Api.BrandApi.CustomerMgmt.action import CustomerAction
from ZapioApi.Api.BrandApi.CustomerMgmt.order_analysis import OrderAnalysis
from ZapioApi.Api.BrandApi.CustomerMgmt.order_listing import CustomerOrders
# 

# Offer setting Configuration
from ZapioApi.Api.BrandApi.offer.offer_create_update import OfferProduct
from ZapioApi.Api.BrandApi.offer.offer_retrieve import OfferRetrieve
from ZapioApi.Api.BrandApi.offer.offer_status import OfferProductaction
from ZapioApi.Api.BrandApi.offer.offer_list import OfferList


# Tag Module
from ZapioApi.Api.BrandApi.tag.tag_create_update import TagCreationUpdation
from ZapioApi.Api.BrandApi.tag.tag_retrieve import TagRetrieve
from ZapioApi.Api.BrandApi.tag.tag_action import TagAction
from ZapioApi.Api.BrandApi.tag.tag_list import TagList

from ZapioApi.Api.BrandApi.Import.customer_excel import CustomerImport
from ZapioApi.Api.BrandApi.is_open import BrandOpen


# Discount Module
from ZapioApi.Api.BrandApi.coupon.coupon_create_update import CouponCreationUpdation
from ZapioApi.Api.BrandApi.coupon.retrieve.coupon import CouponRetrieval
from ZapioApi.Api.BrandApi.coupon.listing.listing import Couponlisting
from ZapioApi.Api.BrandApi.coupon.action.coupon import CouponAction



# Tag Module
from ZapioApi.Api.BrandApi.reason.reason_create_update import ReasonCreationUpdation
from ZapioApi.Api.BrandApi.reason.reason_retrieve import ReasonRetrieve
from ZapioApi.Api.BrandApi.reason.reason_action import ReasonAction
from ZapioApi.Api.BrandApi.reason.reason_list import ReasonList


# Delivery Boy
from ZapioApi.Api.BrandApi.deliveryboy.delivery_create_update import DeliveryBoyRegistration1
from ZapioApi.Api.BrandApi.deliveryboy.delivery_retrieve import DeliveryBoyRetrieve
from ZapioApi.Api.BrandApi.deliveryboy.delivery_status import DeliveryBoyAction
from ZapioApi.Api.BrandApi.deliveryboy.delivery_list import DeliveryList


# Report
from ZapioApi.Api.BrandApi.ordermgmt.csv_order import Ordercsv
from ZapioApi.Api.BrandApi.productdata.product_report import ProductReport
from ZapioApi.Api.BrandApi.productdata.product_csv import ProductReportCsv

from ZapioApi.Api.BrandApi.addons.addon_report import AddonReport
from ZapioApi.Api.BrandApi.addons.addon_csv import AddonReportCsv
from ZapioApi.Api.BrandApi.addons.addon_csv1 import Addoncsv
from ZapioApi.Api.BrandApi.ordermgmt.payment import PaymentReport
from ZapioApi.Api.BrandApi.ordermgmt.payment_csv import PaymentReportCsv
from ZapioApi.Api.BrandApi.ordermgmt.alloutlet import AllOutlet
from ZapioApi.Api.BrandApi.ordermgmt.rating import RatingCSV
from ZapioApi.Api.BrandApi.ordermgmt.ratingUpload import BulkRatingUpdate
from ZapioApi.Api.BrandApi.ordermgmt.outlet_log import AllLog
from ZapioApi.Api.BrandApi.ordermgmt.log_csv import AllLogCsv


# Receipt Module
from ZapioApi.Api.BrandApi.ReceiveConfiguration.receive_create_update import ReceiveCreationUpdation
from ZapioApi.Api.BrandApi.ReceiveConfiguration.receive_retrieve import ReceiveRetrieve
from ZapioApi.Api.BrandApi.ReceiveConfiguration.receive_action import ReceiveAction
from ZapioApi.Api.BrandApi.ReceiveConfiguration.receive_list import ReceiveList


# Receipt Module
from ZapioApi.Api.BrandApi.ordermgmt.edit_order import EditOrder
from ZapioApi.Api.BrandApi.ordermgmt.order_retrieve import OrderRetrieve
from ZapioApi.Api.BrandApi.ordermgmt.allstatus import OrderStatus



urlpatterns = [
	#API Endpoints for brand manager
	path('brand_outlet/outlet_creation/',OutletCreation.as_view()),
	path('brand_outlet/outlet_retreive/',OutletRetreive.as_view()),
	path('configuration_data/outlet_data/',OutletListing.as_view()),
	path('configuration_data/catagory_data/',CatagoryListing.as_view()),
	path('configuration_data/subcatagory_data/',SubCatagoryListing.as_view()),
	path('configuration_data/catwise_outlet_data/',CatagoryWiseOutletListing.as_view()),
	path('configuration_data/catwise_subcat_data/',CatagoryWiseSubCategoryListing.as_view()),
	path('configuration_data/citywise_area_data/',CityWiseAreaListing.as_view()),

	#API Endpoints for brand manager to create & update data
	path('createupdate_data/catagory/',CategoryCreationUpdation.as_view()),
	path('create_data/subcatagory/',SubCategoryCreation.as_view()),
	path('update_data/subcatagory/',SubCategoryUpdation.as_view()),
	path('createupdate_data/foodtype/',FoodTypeCreationUpdation.as_view()),
	path('createupdate_data/variant/',VariantCreationUpdation.as_view()),
	path('createupdate_data/addons/',AddonCreationUpdation.as_view()),
	path('createupdate_data/addonassociation/',AddonAssociateCreationUpdation.as_view()),
	path('createupdate_data/product/',ProductCreationUpdation.as_view()),

	# API Endpoints for brand manager for single data retrieve
	path('retrieval_data/category/',CategoryRetrieval.as_view()),
	path('retrieval_data/subcategory/',SubCategoryRetrieval.as_view()),
	path('retrieval_data/foodtype/',FoodTypeRetrieval.as_view()),
	path('retrieval_data/variant/',VariantRetrieval.as_view()),
	path('retrieval_data/AddonDetails/',AddonDetailsRetrieval.as_view()),
	path('retrieval_data/product/',ProductRetrieval.as_view()),
	path('retrieval_data/featureProduct/',FeatureRetrieval.as_view()),

	# API Endpoints for brand manager for data listing
	path('listing_data/variant/',Variantlisting.as_view()),
	path('listing_data/AddonDetails/',AddonDetailslisting.as_view()),
	path('listing_data/FoodType/',FoodTypelisting.as_view()),
	path('listing_data/City/',Citylisting.as_view()),
	path('listing_data/SubCategory/',SubCategorylisting.as_view()),
	path('listing_data/product/',Productlisting.as_view()),
	path('listing_data/company/',Companylisting.as_view()),
	path('listing_data/feature_product/',FeatureListing.as_view()),
	path('listing_data/userwise_outlet/',UserOutlet.as_view()),

	

	# API Endpoints for brand manager for action
	path('action/product/',ProductAction.as_view()),
	path('action/Category/',CategoryAction.as_view()),
	path('action/subcategory/',SubCategoryAction.as_view()),
	path('action/variant/',VariantAction.as_view()),
	path('action/AddonDetails/',AddonDetailsAction.as_view()),
	path('action/foodtype/',FoodTypeAction.as_view()),
	path('action/Outlet/',OutletAction.as_view()),
	path('action/FeaturedProduct/',FeatureAction.as_view()),

	# API Endpoints for brand manager for profile management
	path('brandprofile/updation/',ProfileUpdation.as_view()),

	# API Endpoints for brand manager for active item listing
	path('Activelisting/variant/',VariantActive.as_view()),
	path('Activelisting/FoodType/',FoodTypeActive.as_view()),
	path('Activelisting/Category/',CategoryActive.as_view()),
	path('Activelisting/AddonDetails/',AddonDetailsActive.as_view()),
	path('Activelisting/Outlet/',Outletlisting.as_view()),
	path('Activelisting/Product/',ActiveProductlisting.as_view()),
	path('Activelisting/Ingredient/',ActiveIngredient.as_view()),

	#API Endpoints for brand manager for product data filter
	path('filterlisting/product/',ProductListFilter.as_view()),
	path('filterlisting/multiplecategory/product/',MultipleCategoryFilter.as_view()),
	path('filterlisting/ActiveTags/',ActiveTagList.as_view()),

	#API Endpoints for brand manager for coupon mgmt
	path('discount/coupon/create_update/',CouponCreationUpdation1.as_view()),
	path('discount/quantitycombo/create_update/',QuantityComboCreationUpdation.as_view()),
	path('discount/percentcombo/create_update/',PercentComboCreationUpdation.as_view()),
	path('discount/coupon/listing/',Couponlisting1.as_view()),
	path('discount/QuantityCombo/listing/',QuantityCombolisting.as_view()),
	path('discount/PercentCombo/listing/',PercentCombolisting.as_view()),
	path('discount/coupon/retrieve/',CouponRetrieval1.as_view()),
	path('discount/QuantityCombo/retrieve/',QuantityComboRetrieval.as_view()),
	path('discount/PercentCombo/retrieve/',PercentComboRetrieval.as_view()),
	path('discount/coupon/action/',CouponAction.as_view()),
	path('discount/QuantityCombo/action/',QuantityComboAction.as_view()),
	path('discount/PercentCombo/action/',PercentComboAction.as_view()),

	# API Endpoints for order processing and placing for brand manager
	path('order/listing/',Orderlisting.as_view()),

	#API Endpoints for Product feature to create & update data
	path('createupdate_data/feature_product/',Feature.as_view()),

	#API Endpoints for Addons
	path('addons/associate/',AssociateAddon.as_view()),

	#API Endpoints for authentication
	path('brand_outlet/login/',BrandOutletlogin.as_view()),
	path('brand_outlet/IposOTPVerify/',IposOTPVerify.as_view()),
	path('brand_outlet/logout/',BrandOutletlogout.as_view()),
	path('brand_outlet/ChangePassword/',ChangePassword.as_view()),
	path('brand_outlet/IsOpen/',BrandOpen.as_view()),
	path('brand_outlet/SetupInfo/',BrandSetupInfo.as_view()),

	
	
	#API Endpoints for outletmgnt
	path('outletmgmt/OutletListing/',OutletIdNamelisting.as_view()),
	path('outletmgmt/Category/',OutletCategorylist.as_view()),
	path('outletmgmt/Product/',OutletProductlist.as_view()),
	path('outletmgmt/Categoryavail/',BrandLevelCategory.as_view()),
	path('outletmgmt/Productavail/',BrandLevelProductavail.as_view()),
	path('outletmgmt/IsOpen/',OutletIsOpen.as_view()),
	path('outletmgmt/Timing/',OutletTiming.as_view()),
	path('outletmgmt/TimeRetrieval/',OutletTimeRetrieval.as_view()),

	#API Endpoints for ordermgnt
	path('ordermgnt/Order/',OrderListingData.as_view()),
	path('ordermgnt/Retrieval/',BrandOrderRetrieval.as_view()),
	path('ordermgnt/ChangeStatus/',ChangeStatusData.as_view()),
	path('ordermgnt/ratingcsv/',RatingCSV.as_view()),
	path('ordermgnt/ratingcsv/upload/',BulkRatingUpdate.as_view()),

	#API Endpoints for Sound Effect on order recieving
	path('sound/status/',SoundStatus.as_view()),
	path('sound/ChangeStatus/',ChangeSound.as_view()),
	# path('ordermgnt/ChangeStatus/',ChangeStatusData.as_view()),

	# path('pushnotify/', PushHome.as_view()),

	# Kitchen All Api
	path('kitchen/createupdate_data/ingredient/',IngredientCreationUpdation.as_view()),
	path('kitchen/action/ingredient/',IngredientAction.as_view()),
	path('kitchen/list/ingredient/',IngredientList.as_view()),
	path('kitchen/retrieve/ingredient/',IngredientRetrieval.as_view()),
	path('kitchen/createupdate_data/stepprocess/',StepprocessCreateUpdate.as_view()),
	path('kitchen/product/stepprocess/list/',StepprocessList.as_view()),
	path('kitchen/product/stepprocess/view/',StepprocessView.as_view()),
	path('kitchen/product/stepprocess/retrieve/',StepprocessRetrieve.as_view()),
	path('kitchen/product/stepprocess/action/',ProcessAction.as_view()),
	path('kitchen/productwiseVariant/',ProductWiseVariant.as_view()),
	path('kitchen/processStep/delete/',StepProcessDelete.as_view()),
	path('kitchen/processStep/between/',StepProcessBetween.as_view()),
	path('kitchen/processStep/remaining/',StepProcessRemaining.as_view()),

	# Notification All Api
	path('notification/ordercount/',orderNotificationCount.as_view()),
	path('notification/seen/',orderNotificationSeen.as_view()),
	path('notification/all/',orderNotificationAll.as_view()),

	# payment configuration
	path('payment/setting/',PaymentConfig.as_view()),
	path('payment/edit/',PaymentEdit.as_view()),
	path('payment/retrieve/',PaymentRetrieve.as_view()),
	path('payment/action/',PaymentAction.as_view()),

	# Theme Setting
	path('theme/setting/',ThemeConfig.as_view()),
	path('theme/edit/',ThemeEdit.as_view()),
	path('theme/retrieve/',ThemeRetrieve.as_view()),
	path('theme/action/',ThemeAction.as_view()),

	# CustomerMgmt
	path('Customer/Active/listing/', ActiveCustomer.as_view()),
	path('Customer/All/listing/', UserlistingSearch.as_view()),
	path('Customer/Action/', CustomerAction.as_view()),
	path('Customer/OrderAnalysis/retrieve/', OrderAnalysis.as_view()),
	path('Customer/OrderHistory/listing/', CustomerOrders.as_view()),

	# Theme Setting
	path('deliverycharge/setting/',DeliveryConfig.as_view()),
	path('deliverycharge/edit/',DeliveryEdit.as_view()),
	path('deliverycharge/action/',DeliveryAction.as_view()),

	# Analytics Setting
	path('Analytics/setting/',AnalyticsConfig.as_view()),
	path('Analytics/edit/',AnalyticsEdit.as_view()),
	path('Analytics/action/',AnalyticsAction.as_view()),


	# Offer setting
	path('offer/product/save/',OfferProduct.as_view()),
	path('offer/product/action/',OfferProductaction.as_view()),
	path('offer/product/retrieve/',OfferRetrieve.as_view()),
	path('offer/product/list/',OfferList.as_view()),


	# Tag Module
	path('tag/createupdate_data/',TagCreationUpdation.as_view()),
	path('tag/action/',TagAction.as_view()),
	path('tag/list/',TagList.as_view()),
	path('tag/retrieve/',TagRetrieve.as_view()),


	path('customer/import/',CustomerImport.as_view()),


	# Discount Module
	path('discount/create_update/',CouponCreationUpdation.as_view()),
	path('discount/retrieve/',CouponRetrieval.as_view()),
	path('discount/list/',Couponlisting.as_view()),
	path('discount/action/',CouponAction.as_view()),


	# Tag Module
	path('reason/createupdate_data/',ReasonCreationUpdation.as_view()),
	path('reason/action/',ReasonAction.as_view()),
	path('reason/list/',ReasonList.as_view()),
	path('reason/retrieve/',ReasonRetrieve.as_view()),


	# Delivery Boy
	path('deliveryboy/create_update/',DeliveryBoyRegistration1.as_view()),
	path('deliveryboy/retrieve/',DeliveryBoyRetrieve.as_view()),
	path('deliveryboy/list/',DeliveryList.as_view()),
	path('deliveryboy/action/',DeliveryBoyAction.as_view()),

	
	# Report Session
	path('product/report/',ProductReport.as_view()),
	path('product/report/csv/',ProductReportCsv.as_view()),
	path('addon/report/',AddonReport.as_view()),
	path('addon/report/csv/',AddonReportCsv.as_view()),
	path('ordermgnt/Order/csv/',Ordercsv.as_view()),
	path('ordermgnt/addon/csv1/',Addoncsv.as_view()),
	path('ordermgnt/payment/report/',PaymentReport.as_view()),
	path('ordermgnt/payment/report/csv/',PaymentReportCsv.as_view()),
	path('ordermgnt/outlet/',AllOutlet.as_view()),
	path('ordermgnt/log/',AllLog.as_view()),
	path('ordermgnt/log/csv/',AllLogCsv.as_view()),
	path('itemlevel/report/',ProductLevelReport.as_view()),
	path('itemlevel/csv/',ProductLevelCSV.as_view()),
	path('dropbox/reportlist/',Dropboxlisting.as_view()),
	# path('itemlevel/quote/',UnprocessedQuote.as_view()),
	path('dropbox/deletereport/',Dropboxdeleting.as_view()),

	# Receive Configuration
	path('receive/createupdate_data/',ReceiveCreationUpdation.as_view()),
	path('receive/action/',ReceiveAction.as_view()),
	path('receive/list/',ReceiveList.as_view()),
	path('receive/retrieve/',ReceiveRetrieve.as_view()),


	# Order Moduel
	path('order/edit/',EditOrder.as_view()),
	path('order/retrieve/',OrderRetrieve.as_view()),
	path('order/allstatus/',OrderStatus.as_view()),

]