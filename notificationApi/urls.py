from django.urls import path
from notificationApi.Api.brand.notification import (orderNotificationCount,
													orderNotificationAll,
													orderNotificationSeen,
													)

from notificationApi.Api.outlet.order_notification import (orderNotificationCount,
													orderNotificationAll,
													orderNotificationSeen,
													)


urlpatterns = [
	path('outlet/ordernotification/count/',orderNotificationCount.as_view()),
	path('outlet/ordernotification/all/',orderNotificationAll.as_view()),
	path('outlet/ordernotification/seen/',orderNotificationSeen.as_view()),

	path('brand/ordernotification/count/',orderNotificationCount.as_view()),
	path('brand/ordernotification/all/',orderNotificationAll.as_view()),
	path('brand/ordernotification/seen/',orderNotificationSeen.as_view()),

]