from django.urls import path
from HistoryApi.Api.coupon_history import  historyCoupon,brandhistoryCoupon
from HistoryApi.Api.customer_history import historyCustomer


urlpatterns = [
	path('outlet/couponHistory/',historyCoupon.as_view()),
	path('brand/couponHistory/',brandhistoryCoupon.as_view()),
	path('outlet/customerHistory/',historyCustomer.as_view()),
]