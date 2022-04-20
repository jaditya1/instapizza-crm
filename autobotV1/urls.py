"""zapio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from autobotV1 import settings

urlpatterns = [
]

import time, threading
from backgroundjobs.jobs import brand_report, outlet_report
from django.db import connections
from backgroundjobs.order_mgr_bot import order_process_log
from backgroundjobs.automail import automail_rhi_report_mgr, automail_sales_report_mgr
from backgroundjobs.data_cleaner import alldata_cleaner





WAIT_SECONDS_for_order_logging = 10
def update_Order_log_data():
	order_report = alldata_cleaner()
	threading.Timer(WAIT_SECONDS_for_order_logging, update_Order_log_data).start()
update_Order_log_data()


# WAIT_SECONDS_for_order_report_mail = 5
# def update_Order_report_mail_data():
# 	order_report = automail_sales_report_mgr()
# 	threading.Timer(WAIT_SECONDS_for_order_report_mail, update_Order_report_mail_data).start()
# update_Order_report_mail_data()

# WAIT_SECONDS_for_rhi_report_mail = 8
# def update_Outlet_rhi_mail_data():
# 	order_report = automail_rhi_report_mgr()
# 	threading.Timer(WAIT_SECONDS_for_rhi_report_mail, update_Outlet_rhi_mail_data).start()
# update_Outlet_rhi_mail_data()

