import re
import os
from ZapioApi.api_packages import *
from django.db.models import Q
from Outlet.models import OutletProfile
import dateutil.parser
from datetime import datetime
from datetime import date
from UserRole.models import ManagerProfile
from Brands.models import Company

 # Validation check
def err_check(data):
	err_message = {}
	if len(data["outlet_ids"]) != 0:
		for i in data["outlet_ids"]:
			try:
				i = int(i)
			except Exception as e:
				err_message["outlet_ids"] = "Outlet is not valid!!"
				break
	else:
		err_message["outlet_ids"] = "Please select at least one outlet!!"
	if data["start_date"] != "" and data["start_date"] != None and data["end_date"] != "" \
		and data["end_date"] != None:
		try:
			start_date = dateutil.parser.parse(data["start_date"]).date()
			end_date = dateutil.parser.parse(data["end_date"]).date()
		except Exception as e:
			err_message["date"] = "Provided date range is not valid!!"
	else:
		err_message["date"] = "Provided date range is not valid!!"
	if any(err_message.values())==True:
		err = {
			"success": False,
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			}
		return err
	else:
		return None


def record_integrity_check(data,auth_user):
	err_message = {}
	single_outlet = data['outlet_ids'][0]
	outlet = OutletProfile.objects.filter(id=single_outlet)
	if outlet.count() == 0:
		to_proceed = 0
		err_message['outlet_ids'] = "Some outlet data is not valid!!"
	else:
		c_id = outlet[0].Company_id
		to_proceed = 1
	if to_proceed == 1:
		for i in data['outlet_ids']:
			q =  OutletProfile.objects.filter(id=i, active_status=1)
			if q.count() == 0:
				err_message['outlet_ids'] = "Some outlet data is not valid!!"
				break
			else:
				if q[0].Company_id == c_id:
					pass
				else:
					err_message['outlet_ids'] = "Please select outlets that belong to same brand!!"
					break
	else:
		pass
	start_date = dateutil.parser.parse(data["start_date"]).date()
	end_date = dateutil.parser.parse(data["end_date"]).date()
	now = datetime.now().date()
	if start_date <= end_date and end_date <= now:
		pass
	else:
		 err_message["date"] = "Please provide meaningful date range!!"
	if any(err_message.values())==True:
		err = {
			"success": False,
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			}
		return err
	else:
		return None