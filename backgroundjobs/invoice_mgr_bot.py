from datetime import datetime,timedelta
import requests
from django.db.models import Q
from Brands.models import Company
from Outlet.models import OutletProfile
from Orders.models import Order
from Location.models import *
from ZapioApi.Api.webhooks.order_live import genrate_invoice_number



def invoice_mgr():
	now = datetime.now()
	time_ago = now - timedelta(days=6)
	record = Order.objects.filter(Q(order_time__gte=time_ago)).order_by('order_time')
	outlet_record = OutletProfile.objects.filter(active_status=1,id=12)
	for i in outlet_record:
		order_record = record.filter(outlet=i.id).order_by('order_time')
		for j in order_record:
			outlet_count = Order.objects.filter(id__lte=j.id,outlet=i.id)
			final_outlet_wise_count = outlet_count.count()+1
			short_name = j.outlet.city.state.short_name
			final_invoice_number = genrate_invoice_number(final_outlet_wise_count)
			finalorderid = str(short_name)+''+str(j.outlet_id)+'-'+str(2021)+''+str(final_invoice_number)
			older_one = j.outlet_order_id
			invoice_update = record.filter(id=j.id).update(outlet_order_id=finalorderid)
	return None