from datetime import datetime
import requests


def verify_otp(mobile_no,otp):
	URL = "https://api.msg91.com/api/v5/otp/verify"
	PARAMS = {}
	PARAMS["authkey"] = "337203Avr8btxDgvq65f20305eP1"
	PARAMS["otp"] = otp
	PARAMS["mobile"] = mobile_no
	response = requests.post(url = URL, params = PARAMS) 
	response_data = response.json()
	if "type" in response_data:
		if response_data["type"] == "success":
			return True
		else:
			return False
	else:
		return False


# verify_otp("917985867241","4149")