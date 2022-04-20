from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from Product.models import Product, Product_availability, Category_availability, \
								ProductCategory, Tag, ProductsubCategory,CachedMenuData
from Outlet.models import OutletProfile
from Brands.models import Company
import re
import os
from ZapioApi.api_packages import *
from UserRole.models import * 
from django.db.models import Q
from frontApi.menu.customize_fun import CustomizeProduct
import datetime
from discount.models import Coupon
from urbanpiper.models import ProductOutletWise
from Configuration.models import TaxSetting
from ZapioApi.api_packages import validation_master_anything, contact_re

def MenuSync(data):
	cache_manage = True
	POSProductAvailableList(data,cache_manage)
	return True


def POSProductAvailableList(data,cache_manage):
	err_message = {}
	err_message["outlet"] = \
			validation_master_anything(str(data["outlet"]),
			"Outlet",contact_re, 1)
	if any(err_message.values())==True:
		err = {
			"success": False,
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			}
		return err
	# user_id = user.id
	# co_id = ManagerProfile.objects.filter(auth_user_id=user_id)[0].Company_id
	chk_outlet = OutletProfile.objects.filter(Q(id=data['outlet']))
	if chk_outlet.count() > 0:
		company_id = chk_outlet[0].Company_id
	else:
		err = {
			"success": False,
			"error" : err_message,
			"message" : "Outlet ID is not found!!"
			}
		return err

	check_cached_data = CachedMenuData.objects.filter(outlet=data["outlet"])
	if check_cached_data.count()==0:
		pass
	else:
		if cache_manage == False:
			cached_data = check_cached_data[0].menu_data
			err = {
				"success":True,
				"message":"Outletwise product listing worked well!!",
				"data":cached_data
				}
			return err
		else:
			pass
	product_q = Product_availability.objects.filter(outlet_id=data["outlet"])
	final_result = []
	coupons = {}
	coupons["coupon_details"] = []
	today = datetime.datetime.now()
	query = Coupon.objects.filter(frequency__gte=1,
						valid_till__gte=today,outlet_id__icontains=str(data["outlet"]))
	if query.count() > 0:
		for i in query:
			coupon = {}
			coupon['coupon_type'] = i.coupon_type
			coupon['coupon_code'] = i.coupon_code
			coupon['frequency'] = i.frequency
			coupon['valid_frm'] = i.valid_frm.strftime("%d/%b/%Y %I:%M %p")
			coupon['valid_till'] = i.valid_till.strftime("%d/%b/%Y %I:%M %p")
			if len(i.product_map) > 0:
				coupon['product'] = []
				a = i.product_map
				for j in range(len(i.product_map)):
					pro = {}
					pro['id'] = a[j]
					pro['product_name'] = Product.objects.filter(id=a[j])[0].product_name
					coupon['product'].append(pro)
			else:
				pass
			coupons["coupon_details"].append(coupon)
	else:
		pass
	final_result.append(coupons)
	if product_q.count() > 0:
		outlet_id = data["outlet"]
		product = Product.objects.filter(active_status=1,Company=company_id)
		product_ids = product_q[0].available_product
		if len(product_ids) != 0:
			for p in product:
				product_dict = {}
				product_dict["id"] = p.id
				urban_product = ProductOutletWise.objects.filter(sync_product__product=p.id)
				product_dict["urban_detail"] = {}
				if urban_product.count() != 0:
					product_dict["urban_detail"]["is_available"] = urban_product[0].is_available
					product_dict["urban_detail"]["product_status"] = urban_product[0].product_status
				else:
					product_dict["urban_detail"]["is_available"] = False
					product_dict["urban_detail"]["product_status"] = 'Disabled'
				product_dict["product_name"] = p.product_name
				product_dict["food_type"] = p.food_type.food_type
				product_dict["priority"] = p.priority
				if p.price == 0:
					a = p.variant_deatils
					if a !=None:
						c = []
						d = []
						for i in a:
							c.append(i['price'])
							d.append(i['discount_price'])
						product_dict["price"] = min(c)
						product_dict["dis_price"] = min(d)
					else:
						product_dict["price"] = ''
						product_dict["dis_price"] = ''
				else:
					product_dict["price"] = p.price
					product_dict["dis_price"] = p.discount_price

				product_dict["description"] = p.product_desc
				product_dict["kot_desc"] = p.kot_desc

				product_dict["tag"] = []
				tag_chk = p.tags
				if isinstance(tag_chk, list):
					for i in range(len(tag_chk)):
						tagg = {}
						tagg['name'] = Tag.objects.filter(id=tag_chk[i])[0].tag_name
						tagg['id'] = Tag.objects.filter(id=tag_chk[i])[0].id
						product_dict["tag"].append(tagg)
				else:
					pass
				product_dict["category_id"] = p.product_category_id
				product_dict["category_name"] = p.product_category.category_name
				product_sub_list = []
				if p.product_subcategory != None:
					product_dict["sub_category_id"] = p.product_subcategory.id
					product_dict["sub_category_name"] = p.product_subcategory.subcategory_name
					product_sub_dict = {}
					product_sub_dict["sub_category_id"] = p.product_subcategory.id
					product_sub_dict["sub_category_name"] = p.product_subcategory.subcategory_name
					product_sub_list.append(product_sub_dict)
					product_dict["sub_category_details"] = product_sub_list
				else:
					product_dict["sub_category_details"] = "N/A"
					product_dict["sub_category_id"] = None
					product_dict["sub_category_name"] = None
				if str(p.id) not in product_ids:
					product_dict["is_available"] = False
				else:
					product_dict["is_available"] = True
				p_list = {}
				p_list['p_id'] = p.id
				p_list['outlet'] = data["outlet"]
				product_dict['customize_detail'] = CustomizeProduct(p_list)
				product_dict["tax_detail"] = []
				associate_tax = p.tax_association
				if associate_tax != None:
					if len(associate_tax) == 0:
						pass
					else:
						for t in associate_tax:
							tax_dict = {}
							tax_q = TaxSetting.objects.filter(id=t)[0]
							tax_dict["id"] = tax_q.id
							tax_dict["tax_name"] = tax_q.tax_name+" | "+str(tax_q.tax_percent)
							tax_dict["tax_percent"] = tax_q.tax_percent
							product_dict["tax_detail"].append(tax_dict)
				else:
					pass
				final_result.append(product_dict)
		else:
			for i in product:
				product_dict = {}
				product_dict["id"] = i.id
				urban_product = ProductOutletWise.objects.filter(sync_product__product=i.id)
				product_dict["urban_detail"] = {}
				if urban_product.count() != 0:
					product_dict["urban_detail"]["is_available"] = urban_product[0].is_available
					product_dict["urban_detail"]["product_status"] = urban_product[0].product_status
				else:
					product_dict["urban_detail"]["is_available"] = False
					product_dict["urban_detail"]["product_status"] = 'Disabled'
				product_dict["product_name"] = i.product_name
				product_dict["is_available"] = False
				product_dict["food_type"] = i.food_type.food_type
				product_dict["priority"] = i.priority
				product_dict["price"] = i.price
				if i.price == 0:
					a = i.variant_deatils
					c = []
					d = []
					for j in a:
						c.append(j['price'])
						d.append(j['discount_price'])
					product_dict["price"] = min(c)
					product_dict["dis_price"] = min(d)
				else:
					product_dict["price"] = i.price
					product_dict["dis_price"] = i.discount_price

				product_dict["dis_price"] = i.discount_price
				product_dict["description"] = i.product_desc
				product_dict["kot_desc"] = i.kot_desc

				product_dict["tag"] = []
				tag_chk = i.tags
				if isinstance(tag_chk, list):
					for i in range(len(tag_chk)):
						tagg = {}
						tagg['name'] = Tag.objects.filter(id=tag_chk[i])[0].tag_name
						tagg['id'] = Tag.objects.filter(id=tag_chk[i])[0].id
						product_dict["tag"].append(tagg)
				else:
					pass
				product_dict["category_id"] = i.product_category
				product_dict["category_name"] = ProductCategory.objects.filter(id=product_dict["category_id"])[0].category_name
				product_dict["tax_detail"] = []
				product_sub_list = []
				if p.product_subcategory != None:
					product_dict["sub_category_id"] = p.product_subcategory.id
					product_dict["sub_category_name"] = p.product_subcategory.subcategory_name
					product_sub_dict = {}
					product_sub_dict["sub_category_id"] = p.product_subcategory.id
					product_sub_dict["sub_category_name"] = p.product_subcategory.subcategory_name
					product_sub_list.append(product_sub_dict)
					product_dict["sub_category_details"] = product_sub_list
				else:
					product_dict["sub_category_details"] = "N/A"
					product_dict["sub_category_id"] = None
					product_dict["sub_category_name"] = None
				associate_tax = i.tax_association
				if associate_tax != None:
					if len(associate_tax) == 0:
						pass
					else:
						for t in associate_tax:
							tax_dict = {}
							tax_q = TaxSetting.objects.filter(id=t)[0]
							tax_dict["id"] = tax_q.id
							tax_dict["tax_name"] = tax_q.tax_name+" | "+str(tax_q.tax_percent)
							tax_dict["tax_percent"] = tax_q.tax_percent
							product_dict["tax_detail"].append(tax_dict)
				else:
					pass
				final_result.append(product_dict)
	else:
		return None
	if len(final_result) > 0:
		if check_cached_data.count() == 0:
			cached_data_create = CachedMenuData.objects.create(outlet_id=data["outlet"],\
													menu_data=final_result)
		else:
			cached_data_update = check_cached_data.update(menu_data=final_result,updated_at=today)
		err = {
			"success":True,
			"message":"Outletwise product listing worked well!!",
			"data":final_result
			}
	else:
		pass
	return err

def POSCategoryAvailableList(data,user):
	err_message = {}
	err_message["outlet"] = \
			validation_master_anything(str(data["outlet"]),
			"Outlet",contact_re, 1)
	if any(err_message.values())==True:
		err = {
			"success": False,
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			}
		return Response(err)
	outlet = OutletProfile.objects.filter(id=data["outlet"],active_status=1)
	if outlet.count() == 0:
		return None
	else:
		user_id = user.id
		cat_q = Category_availability.objects.filter(outlet_id=data["outlet"])
		co_id = outlet[0].Company_id
		category = ProductCategory.objects.filter(active_status=1, Company=co_id)
		final_result = []
		if cat_q.count() == 0:
			create_cat_avail = \
			Category_availability.objects.create(outlet_id=data["outlet"],available_cat=[])
			for p in category:
				cat_dict = {}
				cat_dict["id"] = p.id
				cat_dict["category_name"] = p.category_name
				cat_dict["category_code"] = p.category_code
				cat_dict["priority"] = p.priority
				cat_dict["is_available"] = False
				cat_dict1 = []
				query1 = ProductsubCategory.objects.filter(category=cat_dict["id"], active_status=1)
				for i in query1:
					sub_cat = {}
					sub_cat["sub_c_id"] = i.id
					sub_cat["sub_category_name"] = i.subcategory_name
					sub_cat["sub_ordering"] = i.priority
					cat_dict1.append(sub_cat)
				cat_dict["sub_cat_detail"] = cat_dict1
				final_result.append(cat_dict)
		else:
			cat_ids = cat_q[0].available_cat
			if len(cat_ids) != 0:
				for p in category:
					cat_dict = {}
					cat_dict["id"] = p.id
					cat_dict["category_name"] = p.category_name
					cat_dict["category_code"] = p.category_code
					cat_dict["priority"] = p.priority
					if str(p.id) not in cat_ids:
						cat_dict["is_available"] = False
					else:
						cat_dict["is_available"] = True
					cat_dict1 = []
					query1 = ProductsubCategory.objects.filter(category=cat_dict["id"], active_status=1)
					for i in query1:
						sub_cat = {}
						sub_cat["sub_c_id"] = i.id
						sub_cat["sub_category_name"] = i.subcategory_name
						sub_cat["sub_ordering"] = i.priority
						cat_dict1.append(sub_cat)
					cat_dict["sub_cat_detail"] = cat_dict1
					final_result.append(cat_dict)
			else:
				for p in category:
					cat_dict = {}
					cat_dict["id"] = p.id
					cat_dict["category_name"] = p.category_name
					cat_dict["category_code"] = p.category_code
					cat_dict["priority"] = p.priority
					cat_dict["is_available"] = False
					cat_dict1 = []
					query1 = ProductsubCategory.objects.filter(category=cat_dict["id"], active_status=1)
					for i in query1:
						sub_cat = {}
						sub_cat["sub_c_id"] = i.id
						sub_cat["sub_category_name"] = i.subcategory_name
						sub_cat["sub_ordering"] = i.priority
						cat_dict1.append(sub_cat)
					cat_dict["sub_cat_detail"] = cat_dict1
					final_result.append(cat_dict)
	if len(final_result) > 0:
		err = {
			"success":True,
			"message"		:	"Outletwise category listing worked well!!",
			"data"			:	final_result,
			"Company_id" 	: 	co_id
			}
	else:
		err = None
	return err
