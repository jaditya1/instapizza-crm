from datetime import datetime, timedelta
from Orders.models import Order
from django.db.models import Count, Sum, Max, Avg, Case, When, Value, IntegerField, BooleanField
from django.db.models.functions import ExtractYear, ExtractMonth,ExtractWeek, ExtractWeekDay
from django.db.models.functions import Extract
from backgroundjobs.models import backgroundjobs
from Brands.models import Company
from Outlet.models import OutletProfile
from Product.models import Product, Product_availability
from django.db import connections
from zapio.settings import Media_Path


def brand_report():
	brand = Company.objects.filter(active_status=1)
	for b in brand:
		order_record = Order.objects.filter(Company_id=b.id)
		if order_record.count() == 0:
			pass
		else:
			company_id = order_record[0].Company_id
			now = datetime.now()
			year = now.year
			month = now.month
			today = now.day
			todate = now.date()
			order_result = order_record.values('Company').\
							annotate(total_revenue=Sum('total_bill_value'),order_count=Count("id"))
			
			c = order_record.filter(order_time__year=year,\
				order_time__month=month,order_time__day=today)

			order_today = c.count()
			if order_today > 0:

				tevenue = c.values('Company').\
							annotate(total_revenue=Sum('total_bill_value'),order_count=Count("id"))
				today_revenue = tevenue[0]["total_revenue"]
			else:
				today_revenue = 0
			

			a = datetime.today().date()
			first_day = a.replace(day=1)
			yesterday = now - timedelta(days=1)
			m = order_record.filter(order_time__gte=first_day,order_time__lt=yesterday)
			month = m.count()
			if month > 0:
				mrevenue = m.values('Company').\
							annotate(total_revenue=Sum('total_bill_value'),order_count=Count("id"))
				month_revenue = mrevenue[0]["total_revenue"]
			else:
				month_revenue = 0


			last_week_day = now - timedelta(days=7)
			l_w_order = order_record.filter(order_time__year=last_week_day.year,\
				order_time__month=last_week_day.month,order_time__day=last_week_day.day)
			last_week_order = l_w_order.count()
			if last_week_order > 0:
				lrevenue = l_w_order.values('Company').\
							annotate(total_revenue=Sum('total_bill_value'),order_count=Count("id"))
				last_week_order_revenue = lrevenue[0]["total_revenue"]
			else:
				last_week_order_revenue = 0


			completed_orders = order_record.filter(is_completed=1).count()
			pending_orders = order_record.filter(is_completed=0).count()
			final_result = []
			card_dict = {}
			card_dict["total_revenue"] = order_result[0]["total_revenue"]
			card_dict["total_order"] = order_result[0]["order_count"]
			card_dict["completed_orders"] = completed_orders
			card_dict["pending_orders"] = pending_orders
			card_dict["today_order_count"] = order_today
			card_dict["month_to_yesterday"] = month
			card_dict["last_week_day"] = last_week_order
			card_dict["today_revenue"] = today_revenue
			card_dict["month_to_yesterday_revenue"] = month_revenue
			card_dict["last_week_day_revenue"] = last_week_order_revenue
			


			week_1 = now - timedelta(days=7)
			week_2 = week_1 - timedelta(days=7)
			sales_report_1 = order_record.filter(order_time__gte=now-timedelta(days=7))
			week_1_result = sales_report_1.annotate(weekday=ExtractWeekDay('order_time')).\
											values('weekday').annotate(sales=Sum('total_bill_value')).\
											values('weekday','sales')
			sales_report_2 = order_record.filter(order_time__lte=week_1, order_time__gte=week_2)
			week_2_result = sales_report_2.annotate(weekday=ExtractWeekDay('order_time')).\
											values('weekday').annotate(sales=Sum('total_bill_value')).\
											values('weekday','sales')
			card_dict["week_1_report"] = [0,0,0,0,0,0,0]
			for i in week_1_result:
				if i["weekday"] == 1:
					card_dict["week_1_report"][6] = i["sales"]
				else:
					card_dict["week_1_report"][i["weekday"]-2] = i["sales"]
			card_dict["week_2_report"] = [0,0,0,0,0,0,0]

			for j in week_2_result:
				if j["weekday"] == 1:
					card_dict["week_2_report"][6] = j["sales"]
				else:
					card_dict["week_2_report"][j["weekday"]-2] = j["sales"]

			Outletwise_revenue = \
				c.values('Company','outlet__Outletname').\
						annotate(revenue=Sum('total_bill_value'),order_count=Count("id"))\
						.order_by('-revenue')
			card_dict["outlet_revenue"] = []
			if Outletwise_revenue.count() != 0:
				for j in Outletwise_revenue:
					revenue_dict = {}
					revenue_dict["outlet_name"] = j["outlet__Outletname"]
					revenue_dict["revenue"] = j["revenue"]
					revenue_dict["order_count"] = j["order_count"]
					card_dict["outlet_revenue"].append(revenue_dict)
			else:
				pass
			card_dict["new_customer_report"] = [0,0,0,0,0,0,0]
			card_dict["loyal_customer_report"] = [0,0,0,0,0,0,0]
			current_month_loyal = order_record.filter(order_time__month=now.month,has_been_here=1)
			for i in range(1,8):
				weekday_loyal_count = current_month_loyal.filter(order_time__week_day=i).count()
				if i == 1:
					card_dict["loyal_customer_report"][6] = weekday_loyal_count
				else:
					card_dict["loyal_customer_report"][i-2] = weekday_loyal_count
			current_month_new = order_record.filter(order_time__month=now.month,has_been_here=0)
			for j in range(1,8):
				weekday_new_count = current_month_new.filter(order_time__week_day=j).count()
				if j == 1:
					card_dict["new_customer_report"][6] = weekday_new_count
				else:
					card_dict["new_customer_report"][j-2] = weekday_new_count
			card_dict["order_details"] = []
			today_order = order_record.filter(order_time__date=todate).order_by('-order_time')
			for l in today_order:
				order_dict = {}
				order_dict['id'] = l.id
				order_dict['order_id'] = l.order_id
				order_dict['order_status'] = l.order_status.Order_staus_name
				order_dict['total_bill_value'] = l.total_bill_value
				order_dict['total_items'] = l.total_items
				o_time = l.order_time + +timedelta(hours=5,minutes=30)
				order_dict['order_time'] = o_time.strftime("%d/%b/%y %I:%M %p")
				if l.delivery_time != None:
					order_dict['delivery_time'] = l.delivery_time.strftime("%d/%b/%y %I:%M %p")
				else:
					order_dict['delivery_time'] = None
				order_dict['payment_mode'] = l.get_payment_mode_display()
				order_dict['outlet_name'] = l.outlet.Outletname
				order_dict['is_paid'] = l.is_paid
				order_dict["can_process"] = True
				if l.order_status.can_process == 1:
					pass
				else:
					order_dict["can_process"] = False
				card_dict["order_details"].append(order_dict)
			#For best seller report
			best_seller = order_record.all()
			all_orders = []
			best_list_id = []
			id_wise_freq = {}
			id_wise_price = {}
			for i in best_seller:
				orders = i.order_description
				for o in orders:
					all_orders.append(o)
			for j in all_orders:
				best_list_id.append(j["id"])
				id_wise_price[j["id"]] = int(j["price"])
			for k in best_list_id:
				id_wise_freq[k] = best_list_id.count(k)
			best_seller_map = \
			{k : v * id_wise_price[k] for k, v in id_wise_freq.items() if k in id_wise_price}
			l1 = []
			l2 = []
			l3 = []
			final_best_seller_ids = []
			for l in best_seller_map.values():
				l1.append(l)
			l1.sort(reverse = True)
			for m,n in best_seller_map.items():
				for  o in l1:
					if n == o:
						final_best_seller_ids.append(m)
					else:
						pass
			card_dict["best_seller"] = []
			for p in final_best_seller_ids:
				product_q = Product.objects.filter(id=p)
				if product_q.count() != 0:
					product_dict = {}
					product_dict["id"] = p
					product_dict["product_name"] = product_q[0].product_name
					product_dict["food_type"] = product_q[0].food_type.food_type
					product_dict["product_desc"] = product_q[0].product_desc
					product_dict["product_image"] = str(product_q[0].product_image)
					if product_dict["product_image"] != None and product_dict["product_image"] != "":
						product_dict["product_image"] = Media_Path+product_dict["product_image"]
					else:
						product_dict["product_image"] = None
					card_dict["best_seller"].append(product_dict)
				else:
					pass
			#For best seller report ends here!!
			final_result.append(card_dict)
			data_check = backgroundjobs.objects.filter(Company_id=company_id)
			if data_check.count() == 0:
				data_create = backgroundjobs.objects.create(Company_id=company_id,report=final_result)
			else:
				data_check.update(report=final_result,updated_at=now)
	# close_all = connections.close_all()
	return "I have updated report successfully!!"


def outlet_report():
	outlet = OutletProfile.objects.filter(active_status=1)
	for b in outlet:
		order_record = Order.objects.filter(outlet_id=b.id)
		if order_record.count() == 0:
			# print ("I didn't find any Data to process!!")
			pass
		else:
			outlet_id = order_record[0].outlet_id
			now = datetime.now()
			year = now.year
			month = now.month
			today = now.day
			order_result = order_record.values('Company').\
							annotate(total_revenue=Sum('total_bill_value'),order_count=Count("id"))
			completed_orders = order_record.filter(is_completed=1).count()
			pending_orders = order_record.filter(is_completed=0).count()
			final_result = []
			card_dict = {}
			# card_dict["is_open"] = outlet[0].is_open
			card_dict["total_revenue"] = order_result[0]["total_revenue"]
			card_dict["total_order"] = order_result[0]["order_count"]
			card_dict["completed_orders"] = completed_orders
			card_dict["pending_orders"] = pending_orders
			week_1 = now - timedelta(days=7)
			week_2 = week_1 - timedelta(days=7)
			sales_report_1 = order_record.filter(order_time__gte=now-timedelta(days=7))
			week_1_result = sales_report_1.annotate(weekday=ExtractWeekDay('order_time')).\
											values('weekday').annotate(sales=Sum('total_bill_value')).\
											values('weekday','sales')
			sales_report_2 = order_record.filter(order_time__lte=week_1, order_time__gte=week_2)
			week_2_result = sales_report_2.annotate(weekday=ExtractWeekDay('order_time')).\
											values('weekday').annotate(sales=Sum('total_bill_value')).\
											values('weekday','sales')
			card_dict["week_1_report"] = [0,0,0,0,0,0,0]
			for i in week_1_result:
				if i["weekday"] == 1:
					card_dict["week_1_report"][6] = i["sales"]
				else:
					card_dict["week_1_report"][i["weekday"]-2] = i["sales"]
			card_dict["week_2_report"] = [0,0,0,0,0,0,0]
			for j in week_2_result:
				if j["weekday"] == 1:
					card_dict["week_2_report"][6] = j["sales"]
				else:
					card_dict["week_2_report"][j["weekday"]-2] = j["sales"]
			outlet_to_company = OutletProfile.objects.filter(active_status=1,id=b.id)
			company_id = outlet_to_company[0].Company_id
			overall_revenue = Order.objects.filter(Company_id=company_id)
			Outletwise_revenue = \
				overall_revenue.values('Company','outlet__Outletname').\
						annotate(revenue=Sum('total_bill_value'))
			card_dict["outlet_revenue"] = []
			if Outletwise_revenue.count() != 0:
				for j in Outletwise_revenue:
					revenue_dict = {}
					revenue_dict["outlet_name"] = j["outlet__Outletname"]
					revenue_dict["revenue"] = j["revenue"]
					card_dict["outlet_revenue"].append(revenue_dict)
			else:
				pass
			card_dict["new_customer_report"] = [0,0,0,0,0,0,0]
			card_dict["loyal_customer_report"] = [0,0,0,0,0,0,0]
			current_month_loyal = order_record.filter(order_time__month=now.month,has_been_here=1)
			for i in range(1,8):
				weekday_loyal_count = current_month_loyal.filter(order_time__week_day=i).count()
				if i == 1:
					card_dict["loyal_customer_report"][6] = weekday_loyal_count
				else:
					card_dict["loyal_customer_report"][i-2] = weekday_loyal_count
			current_month_new = order_record.filter(order_time__month=now.month,has_been_here=0)
			for j in range(1,8):
				weekday_new_count = current_month_new.filter(order_time__week_day=j).count()
				if j == 1:
					card_dict["new_customer_report"][6] = weekday_new_count
				else:
					card_dict["new_customer_report"][j-2] = weekday_new_count
			card_dict["order_details"] = []
			today_order = order_record.filter(order_time__month=month).order_by('-order_time')
			for l in today_order:
				order_dict = {}
				order_dict['order_id'] = l.order_id
				order_dict['order_status'] = l.order_status.Order_staus_name
				order_dict['total_bill_value'] = l.total_bill_value
				order_dict['total_items'] = l.total_items
				order_dict['order_time'] = l.order_time.strftime("%d/%b/%y %I:%M %p")
				if l.delivery_time != None:
					order_dict['delivery_time'] = l.delivery_time.strftime("%d/%b/%y %I:%M %p")
				else:
					order_dict['delivery_time'] = None
				order_dict['payment_mode'] = l.get_payment_mode_display()
				order_dict['outlet_name'] = l.outlet.Outletname
				order_dict['is_paid'] = l.is_paid
				card_dict["order_details"].append(order_dict)
			#For best seller report
			best_seller = order_record.all()
			all_orders = []
			best_list_id = []
			id_wise_freq = {}
			id_wise_price = {}
			for i in best_seller:
				orders = i.order_description
				for o in orders:
					all_orders.append(o)
			for j in all_orders:
				best_list_id.append(j["id"])
				id_wise_price[j["id"]] = int(j["price"])
			for k in best_list_id:
				id_wise_freq[k] = best_list_id.count(k)
			best_seller_map = \
			{k : v * id_wise_price[k] for k, v in id_wise_freq.items() if k in id_wise_price}
			l1 = []
			l2 = []
			l3 = []
			final_best_seller_ids = []
			for l in best_seller_map.values():
				l1.append(l)
			l1.sort(reverse = True)
			for m,n in best_seller_map.items():
				for  o in l1:
					if n == o:
						final_best_seller_ids.append(m)
					else:
						pass
			card_dict["best_seller"] = []
			for p in final_best_seller_ids:
				product_q = Product.objects.filter(id=p)
				if product_q.count() != 0:
					product_dict = {}
					product_dict["id"] = p
					product_dict["product_name"] = product_q[0].product_name
					product_dict["food_type"] = product_q[0].food_type.food_type
					product_dict["product_desc"] = product_q[0].product_desc
					product_dict["product_image"] = str(product_q[0].product_image)
					if product_dict["product_image"] != None and product_dict["product_image"] != "":
						product_dict["product_image"] = Media_Path+product_dict["product_image"]
					else:
						product_dict["product_image"] = None
					card_dict["best_seller"].append(product_dict)
				else:
					pass
			#For best seller report ends here!!
			final_result.append(card_dict)
			data_check = backgroundjobs.objects.filter(outlet_id=outlet_id)
			if data_check.count() == 0:
				data_create = backgroundjobs.objects.create(outlet_id=outlet_id,report=final_result)
			else:
				data_check.update(report=final_result,updated_at=now)
	# close_conn = connections.close_all()
	return "I have updated report successfully!!"



# def product_availability():
# 	outlet = OutletProfile.objects.filter(active_status=1)
# 	availability_q = Product_availability.objects.all()
# 	product = Product.objects.filter(active_status=1)
# 	now = datetime.now()
# 	available_product = []
# 	for i in product:
# 		available_product.append(i.id)
# 	for b in outlet:
# 		outlet_availability = Product_availability.objects.filter(outlet_id=b.id)
# 		if outlet_availability.count() == 0:
# 			availability_create = Product_availability.objects.\
# 			create(outlet_id=b.id,available_product=available_product,created_at=now)
# 		else:
# 			pass
# 	return "Product mapped successfully!!"

