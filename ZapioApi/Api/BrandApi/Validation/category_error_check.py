import re
import os
from ZapioApi.api_packages import *
from Product.models import FoodType, Product, ProductCategory, ProductsubCategory,\
	AddonDetails
from django.db.models import Q
from Outlet.models import OutletProfile
from django.db.models import Max

 # Validation check
def err_check(data):
	err_message = {}
	err_message["category_name"] = \
					validation_master_anything(data["category_name"],
					"Category name",username_re, 3)
	err_message["category_code"] = \
			validation_master_anything(data["category_code"],
			"Category code", username_re, 3)
	err_message["company_auth_id"] = \
			only_required(data["company_auth_id"],"Company")
	err_message["priority"] = \
			validation_master_anything(str(data["priority"]),
			"Priority", contact_re, 1)
	if any(err_message.values())==True:
		err = {
			"success": False,
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			}
		return err
	else:
		return None


def unique_record_check(data,auth_id):
	err_message = {}
	if "id" in data:
		unique_check = ProductCategory.objects.filter(~Q(id=data["id"]),\
			Q(category_name__iexact=data["category_name"]),\
			Q(Company=auth_id))
	else:
		unique_check = ProductCategory.objects.filter(Q(category_name__iexact=data["category_name"]),\
								Q(Company=auth_id))
	if unique_check.count() != 0:
		err_message["unique_check"] = "Category with this name already exists!!"
	else:
		pass
	if "id" in data:
		unique_code_check = ProductCategory.objects.filter(~Q(id=data["id"]),\
			Q(category_code__iexact=data['category_code']),\
			Q(Company=auth_id))
	else:
		unique_code_check = \
		ProductCategory.objects.filter(Q(category_code__iexact=data['category_code']),\
													Q(Company=auth_id))
	if unique_code_check.count() != 0:
		err_message["unique_code_check"] = "Category with this code already exists!!"
	else:
		pass
	if "id" in data:
		priority_check = ProductCategory.objects.filter(~Q(id=data["id"]),\
						Q(priority=int(data["priority"])),Q(Company=auth_id))
	else:
		priority_check = ProductCategory.objects.filter(Q(priority=int(data["priority"])),\
									Q(Company=auth_id))
	if priority_check.count() != 0:
		max_priority = \
		ProductCategory.objects.aggregate(Max('priority'))
		suggestion = max_priority["priority__max"] + 1
		err_message["priority_check"] = \
		"This priority is already assigned to other Category..You can try "+str(suggestion)+" as priority!!"
	else:
		pass
	if any(err_message.values())==True:
		err = {
			"success": False,
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			}
		return err
	else:
		return None