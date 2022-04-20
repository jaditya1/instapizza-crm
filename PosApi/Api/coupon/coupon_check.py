from Product.models import ProductCategory, Product_availability, Category_availability, Product,\
Variant,AddonDetails
import re
from django.conf import settings
from ZapioApi.api_packages import *
from datetime import datetime
from django.db.models import Q
import datetime
from discount.models import Coupon

def check_coupon(data,ccode):
	actual_response = {}
	product_data = data['cart']
	subtotalprice = 0
	Old_subtotal  = 0
	new_subtotal = 0
	tdaprice = 0
	coupon_applied = 0
	percent_type = 1
	today = datetime.datetime.now()
	# is_applied = 0
	query = Coupon.objects.filter(coupon_code__exact=ccode,frequency__gte=1,
							valid_till__gte=today)
	if query.count()!=0:
		is_min_shoppping = query[0].is_min_shop
		for i in range(len(product_data)):
			pname = product_data[i]['name']
			pprice = product_data[i]['details']['actualPrice'] # old price
			pid = str(product_data[i]['id'])
			quantity = product_data[i]['quantity']
			nprice = pprice / quantity
			coupon_checking = coupon_integrity(query)
			if len(coupon_checking) != 0:
				q = query[0]
				mapped_products = q.product_map
				if q.coupon_type == "Flat" and coupon_applied == 0:
					if pid in mapped_products:
						tdaprice = tdaprice+q.flat_discount
						fprice = pprice - q.flat_discount
						coupon_applied = 1
					else:
						fprice = pprice
				elif q.coupon_type == "Percentage" and percent_type == 1:
					if pid in mapped_products:
						daprice = nprice*q.flat_percentage/100
						tdaprice = tdaprice+daprice
						fprice = pprice - daprice
						coupon_applied = 1
					else:
						fprice = pprice
			else:
				q = query[0]
				if q.coupon_type == "Flat" and coupon_applied == 0:
					tdaprice = tdaprice+q.flat_discount
					fprice = pprice - q.flat_discount
					coupon_applied = 1
				elif q.coupon_type == "Percentage" and percent_type == 1:
					daprice = nprice*q.flat_percentage/100
					tdaprice = tdaprice+daprice
					fprice = pprice - daprice
					coupon_applied = 1
				else:
					fprice = pprice
			Old_subtotal = Old_subtotal + pprice
			subtotalprice = subtotalprice + fprice
			if 'toppings' in product_data[i]:
				toppings = product_data[i]['toppings']['addons']
				crustPrice = product_data[i]['toppings']['crustPrice']
				subtotalprice = subtotalprice + crustPrice - pprice
				Old_subtotal = Old_subtotal + crustPrice - pprice
				lent0 = len(toppings)
				if lent0 > 0 :
					ttprice = 0
					for j in range(len(toppings)):
						tprice = toppings[j]['price']
						name = toppings[j]['name']
						ttprice = ttprice + tprice
					subtotalprice = subtotalprice + ttprice
					Old_subtotal = Old_subtotal + ttprice
				else:
					ttprice = 0
			else:
				ttprice = 0
		if is_min_shoppping == True:
			if Old_subtotal<query[0].min_shoping:
				coupon_applied=0
			else:
				pass
			if Old_subtotal>query[0].max_shoping:
				coupon_applied=0
			else:
				pass
		else:
			pass
	else:
		pass
	actual_response["subtotalprice"] = subtotalprice
	actual_response["Old_subtotal"] = Old_subtotal
	actual_response["coupon_applied"] = coupon_applied
	actual_response["tdaprice"] = tdaprice
	return actual_response


def coupon_integrity(query):
	if query.count() > 0:
		q = query[0]
		mapped_products = q.product_map
		if mapped_products==None or mapped_products=="":
			mapped_cat = q.category_id
			if mapped_cat != None:
				products = Product.objects.filter(product_category=mapped_cat,active_status=1)
				p_ids = []
				if products.count() != 0:
					for i in products:
						p_ids.append(str(i.id))
				else:
					pass
				mapped_products = p_ids
			else:
				mapped_products = []
		else:
			p_ids = []
			for j in mapped_products:
				products = Product.objects.filter(id=j,active_status=1)
				if products.count() != 0 :
					p_ids.append(str(j))
				else:
					pass
			mapped_products = p_ids
	else:
		mapped_products = []
	return mapped_products
