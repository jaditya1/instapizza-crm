import re
from ZapioApi.api_packages import *


 # Validation check
def err_check(data):
	err_message = {}
	err_message["username"] = \
			validation_master_anything(data["username"],
			"Username",username_re, 3)
	err_message["password"] = \
			validation_master_anything(data["password"],
			"Password", pass_re, 6)
	err_message["Outletname"] = \
			validation_master_anything(data["Outletname"],
			"Outlet Name", outlet_name_re, 3)
	err_message["pincode"] = \
			validation_master_anything(str(data["pincode"]),
			"Pincode", contact_re, 5)
	err_message["address"] = \
			validation_master_anything(data["address"],
			"Address", address_re, 3)
	err_message["city"] = \
			only_required(data["city"],"City")
	err_message["area"] = \
			only_required(data["area"],"Area")
	err_message["gst"] = \
			only_required(data["gst"],"GST")
	if any(err_message.values())==True:
		err = {
			"success": False,
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			}
		return err
	else:
		return None

def err_check_update(data):
	err_message = {}
	err_message["Outletname"] = \
			validation_master_anything(data["Outletname"],
			"Outlet Name", outlet_name_re, 3)
	err_message["address"] = \
			validation_master_anything(data["address"],
			"Address", address_re, 3)
	err_message["pincode"] = \
			validation_master_anything(str(data["pincode"]),
			"Pincode", contact_re, 5)
	err_message["city"] = \
			only_required(data["city"],"City")
	err_message["area"] = \
			only_required(data["area"],"Area")
	err_message["gst"] = \
			only_required(data["gst"],"GST")
	if any(err_message.values())==True:
		err = {
			"success": False,
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			}
		return err
	else:
		return None