import re
import os
from ZapioApi.api_packages import *
from UserRole.models import UserType
from django.db.models import Q
from django.db.models import Max
from UserRole.models import ManagerProfile
from django.contrib.auth.models import User
from Outlet.models import *

 # Validation check
def err_check(data):
	err_message = {}
	if len(data["outlet"]) != 0:
		outlet_unique_list = []
		for i in data["outlet"]:
			err_message["outlet_map"] = \
				validation_master_anything(str(i),
				"Outlet",contact_re, 1)
			if err_message["outlet_map"] != None:
				break
			if i not in outlet_unique_list:
				outlet_unique_list.append(i)
			else:
				err_message["duplicate_outlet"] = "Outlet are duplicate!!"
				break
			record_check = OutletProfile.objects.filter(Q(id=i),Q(active_status=1))
			if record_check.count() == 0:
				err_message["outlet"] = \
				"Outlet is not valid!!"
				break
	else:
		err_message["outlet"] = "Please Enter Outlet ID"
	err_message["username"] = \
			validation_master_anything(data["username"],"Username", username_re,2)
	if "id" in data:
		err_message["id"] = \
			validation_master_anything(data["id"],"Manager Id", contact_re,1)
	else:
		pass
	err_message["user_type"] = \
			validation_master_anything(str(data["user_type"]),"User Type", contact_re,1)
	err_message["manager_name"] = \
			validation_master_anything(data["manager_name"],"Name", username_re,3)
	err_message["password"] = \
			validation_master_anything(data["password"],"Password", username_re,3)
	err_message["email"] = \
			validation_master_anything(data["email"],"Email", email_re,3)	
	err_message["mobile"] = \
			validation_master_anything(data["mobile"],"Mobile", contact_re,10)	
	if any(err_message.values())==True:
		err = {
			"success": False,
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			}
		return err
	else:
		return None


def record_integrity_check(data,auth_id):
	err_message = {} 
	if "id" in data:
		pass
	else:
		user_already_exist = User.objects.filter(username=data["auth_username"])
		if user_already_exist.count()==1:
			err_message = {}
			err_message["duplicate"] = \
			"User with the entered username already exists..Please try other!!"
		else:
			pass
	if "id" in data:
		unique_check = ManagerProfile.objects.filter(~Q(id=data["id"]),\
			Q(username=data["username"]))
	else:
		unique_check = ManagerProfile.objects.filter(Q(username=data["username"]))
	if unique_check.count() != 0:
		err_message["username"] = "This user name is already assigned to someone else!!"
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