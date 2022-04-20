from django.urls import path, include
from PosApi.Api.Authorization.pos_login import Poslogin,Poslogout, PosOTPVerify

from PosApi.Api.Authorization.password_verify import PasswordVerify

from PosApi.Api.Authorization.automatic_login import AutomaticLogin

from PosApi.Api.Authorization.pos_userdetail import PosUserDetail
from PosApi.Api.Authorization.pos_changepassword import Changepassword
from PosApi.Api.Authorization.profile_update import ProfileUpdate
from PosApi.Api.order.order_detail import OrderDetail
from PosApi.Api.outletmgmt.listing.outlet_list import AllOutlet

from PosApi.Api.outletmgmt.availability.product import PosLevelProductavail
from PosApi.Api.outletmgmt.availability.category import PosLevelCategory
from PosApi.Api.outletmgmt.availability.variant import PosLevelVariantavail
from PosApi.Api.outletmgmt.availability.addons import PosLevelAddonavail

from PosApi.Api.outletmgmt.outletwiselisting.product import OutletProductlist
from PosApi.Api.outletmgmt.outletwiselisting.category import OutletCategorylist
from PosApi.Api.outletmgmt.outletwiselisting.customize import PosCustomData
from PosApi.Api.outletmgmt.outletwiselisting.addonGrp import OutletwiseAddonGroup
from PosApi.Api.outletmgmt.outletwiselisting.addon import OutletwiseAddons


from PosApi.Api.outletmgmt.is_open import OutletIsOpen
from PosApi.Api.order.order_process import ProcessList
from PosApi.Api.order.order import OrderProcess



from PosApi.Api.ordermgmt.listing import OrderListingData
from PosApi.Api.ordermgmt.order_log import OrderLogData
from PosApi.Api.ordermgmt.change_status import ChangeStatusData
from PosApi.Api.ordermgmt.retrieve import BrandOrderRetrieval
from PosApi.Api.Customer.customer_search import CustomerList
from PosApi.Api.Customer.customer_registration import CustomerRegister
from PosApi.Api.Customer.customer_order import CustomerWiseOrder

from PosApi.Api.menu.customization import CustomeMgmt
from PosApi.Api.notification.notification import orderNotificationCount,orderAccepted,orderNotificationSeen
from PosApi.Api.coupon.discounts import CouponcodeView
from PosApi.Api.coupon.all_discount import AllDiscount
from PosApi.Api.order.order_settle import OrderSettle
from PosApi.Api.order.order_orderid_update import OrderIDUpdate
from PosApi.Api.order.settlebill import OrderBillSettle


#  Rider Api
from PosApi.Api.Rider.allrider import RiderList
from PosApi.Api.Rider.assign_rider import AsignRider

# Temperature tracking
# from PosApi.Api.tempTracker.staff_listing import Stafflisting
from PosApi.Api.tempTracker.latest_temp import TempRetrieve
from PosApi.Api.tempTracker.add_temp import TempAdd
from PosApi.Api.tempTracker.invoice_data import InovoiceData

from PosApi.Api.order.service_distance_check import ServiceCheck

urlpatterns = [

	path('user/login/',Poslogin.as_view()),
	path('user/logout/',Poslogout.as_view()),
	path('user/PosOTPVerify/',PosOTPVerify.as_view()),
	path('user/posuser/list/',PosUserDetail.as_view()),
	path('user/posuser/cpass/',Changepassword.as_view()),
	path('user/profile/update/',ProfileUpdate.as_view()),
	path('user/orderdetail/',OrderDetail.as_view()),
	path('user/automatic/login/',AutomaticLogin.as_view()),
	path('user/PasswordVerify/',PasswordVerify.as_view()),

	# Outlet List
	path('outletmgmt/list/',AllOutlet.as_view()),
	path('outletmgmt/Categorylist/',OutletCategorylist.as_view()),
	path('outletmgmt/PosCustomData/',PosCustomData.as_view()),
	path('outletmgmt/Productlist/',OutletProductlist.as_view()),
	path('outletmgmt/OutletwiseAddonGroup/',OutletwiseAddonGroup.as_view()),
	path('outletmgmt/OutletwiseAddons/',OutletwiseAddons.as_view()),
	path('outletmgmt/IsOpen/',OutletIsOpen.as_view()),

	# Availability
	path('outletmgmt/Categoryavail/',PosLevelCategory.as_view()),
	path('outletmgmt/Productavail/',PosLevelProductavail.as_view()),
	path('outletmgmt/PosLevelVariantavail/',PosLevelVariantavail.as_view()),
	path('outletmgmt/PosLevelAddonavail/',PosLevelAddonavail.as_view()),

	# Order Management
	path('order/processlist/',ProcessList.as_view()),
	path('ordermgnt/Order/',OrderListingData.as_view()),
	path('ordermgnt/Order/log/',OrderLogData.as_view()),
	path('ordermgnt/Retrieval/',BrandOrderRetrieval.as_view()),
	path('ordermgnt/ChangeStatus/',ChangeStatusData.as_view()),
	path('ordermgnt/Orderprocess/',OrderProcess.as_view()),
	path('order/settle/',OrderSettle.as_view()),
	path('order/billsettle/',OrderBillSettle.as_view()),

	# Product Customize
	path('product/customize_data/',CustomeMgmt.as_view()),


	# New Order Notification
	path('ordernotification/list/',orderNotificationCount.as_view()),
	path('ordernotification/accepted/',orderAccepted.as_view()),
	path('ordernotification/seen/',orderNotificationSeen.as_view()),

	# New Order Notification
	path('customer/list/',CustomerList.as_view()),
	path('customer/registration/',CustomerRegister.as_view()),
	path('customer/order/',CustomerWiseOrder.as_view()),
	path('couponcode/',CouponcodeView.as_view()),
	path('alldiscount/',AllDiscount.as_view()),
	path('outletid/update/',OrderIDUpdate.as_view()),


	# Rider API
	path('rider/outletwiserider/',RiderList.as_view()),
	path('rider/outletwiserider/assign/',AsignRider.as_view()),


	path('ServiceCheck/',ServiceCheck.as_view()),

	# Temperature API
	path('temp/inovoicedata/', InovoiceData.as_view()),
	path('temp/retrieve/', TempRetrieve.as_view()),
	path('temp/add/', TempAdd.as_view()),

]

