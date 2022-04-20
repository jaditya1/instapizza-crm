from datetime import datetime
import requests
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework import serializers
from django.http import HttpResponse
from Orders.models import Order,OrderStatusType,OrderTracking, OrderProcessTimeLog
from rest_framework.permissions import IsAuthenticated
import dateutil.parser
from Brands.models import Company
from Outlet.models import OutletProfile
from rest_framework.authtoken.models import Token
from UserRole.models import ManagerProfile
from datetime import datetime, timedelta
import secrets
from urbanpiper.models import ProductSync, UrbanOrders
from Product.models import Addons
from withrun.models import *
from django.db import connections
from Configuration.models import TaxSetting
from django import db
import dateutil.parser
import time
from django.utils import timezone

def order_process_log():
	record = \
	Order.objects.filter(Q(order_status=5),Q(is_logged=0))
	if record.count() != 0:
		for i in record:
			to_log = 1
			track_initial = OrderTracking.objects.filter(order=i.id)
			track = track_initial.filter(Order_staus_name=1)
			if track.count() == 0:
				to_log = 0
			else:
				pass
			accept_track = track_initial.filter(Order_staus_name=2)
			if accept_track.count() == 0:
				to_log = 0
			else:
				pass
			food_ready_track = track_initial.filter(Order_staus_name=3)
			if food_ready_track.count() == 0:
				to_log = 0
			else:
				pass
			dispatch_track = track_initial.filter(Order_staus_name=4)
			if dispatch_track.count() == 0:
				to_log = 0
			else:
				pass
			if to_log == 1:
				place_time = track[0].created_at
				accept_time = accept_track[0].created_at
				order_acceptance_time = ((accept_time - place_time).total_seconds())/60

				food_ready_time = food_ready_track[0].created_at
				kpt = ((food_ready_time - accept_time).total_seconds())/60

				dispatch_time = dispatch_track[0].created_at

				kpt_to_dispatch = ((dispatch_time - food_ready_time).total_seconds())/60
			else:
				order_acceptance_time = 1
				kpt = 7
				kpt_to_dispatch = 5



			record_check = OrderProcessTimeLog.objects.filter(order_id=i.id)
			if record_check.count() == 0:
				record_create = \
				OrderProcessTimeLog.objects.create(order_id=i.id,\
								order_acceptance_time=order_acceptance_time,\
								kpt=kpt,kpt_to_dispatch=kpt_to_dispatch)
			else:
				record_update = record_check.update(order_acceptance_time=order_acceptance_time,\
								kpt=kpt,kpt_to_dispatch=kpt_to_dispatch)
			main_order_update =  Order.objects.filter(id=i.id).update(is_logged=1)
	else:
		pass
	return "OrderProcessTimeLog__done"