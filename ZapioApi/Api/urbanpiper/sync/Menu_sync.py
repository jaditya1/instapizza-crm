from urbanpiper.models import UrbanCred, APIReference, EventTypes
import requests
import json



def menu_sync(data,company_id, outlet_id):
	url = "https://api.urbanpiper.com/external/api/v1/inventory/locations/"+str(outlet_id)+"/"
	# url = "https://staging.urbanpiper.com/external/api/v1/inventory/locations/"+str(outlet_id)+"/"
	# url = "https://pos-int.urbanpiper.com/external/api/v1/inventory/locations/"+str(outlet_id)+"/"
	data = data
	q = UrbanCred.objects.filter(company_id=company_id,active_status=1)
	if q.count() == 0:
		return None
	else:
		try:
			apikey = q[0].apikey
			username = q[0].username
			headers = {}
			# headers["Authorization"] = \
			# "apikey biz_adm_clients_NNNNZcVEzJyi:fc4361c28ca3cf52928407781bf0952da2d379ea"
			headers["Authorization"] = "apikey "+ username +":"+apikey
			headers["Content-Type"] = "application/json"
			response = requests.request("POST", url, data=json.dumps(data), headers=headers)
			response_data = response.json()
			event_type_q = EventTypes.objects.filter(company=company_id,event_type="inventory_update")
			if event_type_q.count() == 0:
				return None
			else:
				event_type_id = event_type_q[0].id
			if response_data["status"] != "error":
				record_create = \
				APIReference.objects.create(company_id=company_id,event_type_id=event_type_id,\
												ref_id=response_data["reference"],
												api_response=response_data,outlet_id=outlet_id)
			else:
				record_create = \
				APIReference.objects.create(company_id=company_id,event_type_id=event_type_id,\
												ref_id=response_data["reference"],
												error_api_response=response_data,outlet_id=outlet_id)
			return response_data
		except Exception as e:
			return str(e)