import requests
import json
from urbanpiper.models import UrbanCred



def webhooksubscribe(company_id,event_type,callbackurl):
	cred_record = UrbanCred.objects.filter(company=company_id,active_status=1)
	if cred_record.count() == 1:
		username = cred_record[0].username
		apikey = cred_record[0].apikey
		url = 'https://api.urbanpiper.com/external/api/v1/webhooks/'
		data = {}
		data["active"] = True
		data["event_type"] = event_type
		data["retrial_interval_units"] = "seconds"
		data["url"] = callbackurl
		headers = {}
		headers["Authorization"] = "apikey "+ username +":"+apikey
		headers["Content-Type"] = "application/json"
		headers["cache-control"] = "no-cache"
		headers["x_api_token"] = "4trgfdsfd243tg54342rewfcef"
		response = requests.request("POST", url, data=json.dumps(data), headers=headers)
		# response = requests.request("POST", url, data=json.dumps(data), headers=headers)
		data = response.json()
		return data
	else:
		return {"message" : "UrbanPiper Credentials are not set properly!!"}


def webhook_update(q):
	cred_record = UrbanCred.objects.filter(company=q.company,active_status=1)
	if cred_record.count() == 1:
		webhook_id = str(q.api_response["webhook_id"])
		username = cred_record[0].username
		apikey = cred_record[0].apikey
		url = 'https://api.urbanpiper.com/external/api/v1/webhooks/'+webhook_id+'/'
		data = {}
		data["active"] = True
		data["event_type"] =q.event_type.event_type
		data["retrial_interval_units"] = "seconds"
		data["url"] = q.callbackurl
		headers = {}
		headers["Authorization"] = "apikey "+ username +":"+apikey
		headers["Content-Type"] = "application/json"
		headers["cache-control"] = "no-cache"
		headers["x_api_token"] = "4trgfdsfd243tg54342rewfcef"
		response = requests.request("PUT", url, data=json.dumps(data), headers=headers)
		# response = requests.request("POST", url, data=json.dumps(data), headers=headers)
		data = response.json()
		print(data)
		return data
	else:
		return {"message" : "UrbanPiper Credentials are not set properly!!"}