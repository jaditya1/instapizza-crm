from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from urbanpiper.models import UrbanCred, APIReference, EventTypes,MenuPayload
import requests
import json
from Brands.models import Company
from .master_flush_deassociate import master_flush_menu
from rest_framework_tracking.mixins import LoggingMixin


def flush_menu(company_id,data):
	url = "https://api.urbanpiper.com/external/api/v1/inventory/locations/-1/"
	# url = "https://staging.urbanpiper.com/external/api/v1/inventory/locations/-1/"
	# url = "https://pos-int.urbanpiper.com/external/api/v1/inventory/locations/-1/"
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
			event_type_q = \
			EventTypes.objects.filter(company=company_id,event_type="inventory_update")
			if event_type_q.count() == 0:
				return None
			else:
				event_type_id = event_type_q[0].id
			ref_q = APIReference.objects.all()
			if ref_q.count() == 0:
				last_id = "001"
			else:
				last_id = str(ref_q.last().id+1)
			if response_data["status"] != "error":
				if "reference" not in response_data:
					response_data["reference"] = "unknown-"+last_id
				else:
					pass
				record_create = \
				APIReference.objects.create(company_id=company_id,event_type_id=event_type_id,\
												ref_id=response_data["reference"],
												api_response=response_data)
			else:
				if "reference" not in response_data:
					response_data["reference"] = "unknown-"+last_id
				else:
					pass
				record_create = \
				APIReference.objects.create(company_id=company_id,event_type_id=event_type_id,\
												ref_id=response_data["reference"],
												error_api_response=response_data)
			return response_data
		except Exception as e:
			return str(e)




class MasterFlush(LoggingMixin,APIView):
	"""
	Master Flush GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to flush out all menus accross all
		outletwise with UrbanPiper.

	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		try:
			query = Company.objects.filter(auth_user=request.user.id)
			if query.count() == 0:
				return Response({
					"success" 	: 	False,
					"message"	:	"You are authorized to do this operation!!"
					})
			else:
				company_id = query[0].id
			# flush_data = {}
			# flush_data["flush_categories"] = True
			# flush_data["flush_items"] = True
			# flush_data["flush_option_groups"] = True
			# flush_data["flush_options"] = True
			# flush_data["categories"] = []
			# flush_data["items"] = []
			# flush_data["option_groups"] = []
			# flush_data["options"] = []
			# flush_data["taxes"] = []
			# flush_data["charges"] = []

			# cat_dict = {}
			# if company_id == 1:
			# 	cat_dict["ref_id"] = "Dummy-Insta-cat-1001"
			# 	cat_dict["name"] = "Dummy Instapizza Category"
			# else:
			# 	cat_dict["ref_id"] = "Dummy-Sub-cat-1002"
			# 	cat_dict["name"] = "Dummy Subfresh Category"
			# cat_dict["description"] = None
			# cat_dict["sort_order"] = 0
			# cat_dict["active"] = True
			# cat_dict["img_url"] = None
			# cat_dict["parent_ref_id"] = None
			# flush_data["categories"].append(cat_dict)

			# product_dict = {}
			# if company_id == 1:
			# 	product_dict["ref_id"] = "Dummy-Insta-Item-5001"
			# 	product_dict["title"] = "Dummy Instapizza Item"
			# 	product_dict["category_ref_ids"] = ["Dummy-Insta-cat-1001"]
			# else:
			# 	product_dict["ref_id"] = "Dummy-Subfresh-Item-5002"
			# 	product_dict["title"] = "Dummy Subfresh Item"
			# 	product_dict["category_ref_ids"] = ["Dummy-Insta-cat-1002"]

			# product_dict["price"] = 1.0
			# product_dict["description"] = None
			# product_dict["sold_at_store"] = True
			# product_dict["available"] = True
			# product_dict["sort_order"] = 0
			# product_dict["current_stock"] = -1 
			# product_dict["food_type"] = 1
			# product_dict['img_url'] = None
			# product_dict["recommended"] = False
			# product_dict["translations"] = []
			# product_dict["language"] = []
			# product_dict["tags"] = {}
			# product_dict["excluded_platforms"] = ['zomato','swiggy']
			# product_dict["included_platforms"] = []
			# flush_data["items"].append(product_dict)

			# flush_all = flush_menu(company_id,flush_data)
			user = request.user.id
			flush_data = master_flush_menu(company_id, user)

			if  "status" not in flush_data:
				pass
			else:
				return Response (flush_data)
			payload_create = \
			MenuPayload.objects.create(company_id=company_id,payload=flush_data,\
													plateform = "Master Flush")

			flush_all = flush_menu(company_id,flush_data)
			if flush_all == None:
				return Response({
					"status"	:	False,
					"message" 	: 	"Master flush initiation is unsuccessfull!!"
							})
			else:
				pass
			return Response({
							"status":True,
							"message" : "Master flush is initiated successfully!!"
							})
		except Exception as e:
			return Response(
						{"error":str(e)}
						)