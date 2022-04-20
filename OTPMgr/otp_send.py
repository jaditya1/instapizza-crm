from datetime import datetime
import requests


def send_otp(mobile_no,otp_type):
	URL = "https://api.msg91.com/api/v5/otp"
	PARAMS = {}
	PARAMS["authkey"] = "337203Avr8btxDgvq65f20305eP1"
	PARAMS["template_id"] = "5f2bf778d6fc05529f27e74a"
	PARAMS["mobile"] = mobile_no
	PARAMS["otp_expiry"] = 10
	response = requests.get(url = URL, params = PARAMS) 
	response_data = response.json()
	return "Success"


def send_otp_to_pos(mobile_no):
	URL = "https://api.msg91.com/api/v5/otp"
	PARAMS = {}
	PARAMS["authkey"] = "337203Avr8btxDgvq65f20305eP1"
	PARAMS["template_id"] = "5f2ba18fd6fc053e055d96dd"
	PARAMS["mobile"] = mobile_no
	PARAMS["otp_expiry"] = 11
	response = requests.get(url = URL, params = PARAMS) 
	response_data = response.json()
	return "Success"



# send_otp("917985867241","khkj")