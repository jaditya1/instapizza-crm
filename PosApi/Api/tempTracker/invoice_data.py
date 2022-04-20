from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import re
from Outlet.models import TempTracking, OutletProfile
from UserRole.models import ManagerProfile
from datetime import datetime, timedelta
from .latest_temp import secret_token 
from zapio.settings import Media_Path


class InovoiceData(APIView):
	"""
	Invoice data retrieval Post API

		Authentication Required		 	: 		Yes
		Service Usage & Description	 	: 		This Api is used to provide invoice data outletwise.

		Data Post: {

			"id"        : 	"21"
		}

		Response: {

			"success"	: 	True,
			"data"		:	result, 
			"message"	: 	"API worked well!!"

		}

	"""
	# permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			getdata = request.META
			if 'HTTP_TOKEN' in getdata:
				pass
			else:
				return Response({
					"success" : False,
					"message" : "Credentials Not provided!!"
					})
			token = getdata['HTTP_TOKEN']
			if token != secret_token:
				return Response({
					"success" : False,
					"message" : "Provided Credentials do'nt match!!"
					})
			else:
				pass
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			err_message = {}
			err_message["outlet"] = \
				validation_master_anything(str(data["id"]),"Outlet",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
								"success": False,
								"error" : err_message,
								"message" : "Please correct listed errors!!"
							})
			data['id'] = str(data['id'])
			today = datetime.now().date()
			check_company = OutletProfile.objects.filter(active_status=1,id=data['id'])
			if check_company.count()==0:
				return Response(
					{
						"success": False,
	 					"message": "This Company is not active yet !!"
					}
					) 
			else:
				today = datetime.now().date()
				final_result = []
				for outlet in check_company:
					out_dict = {}
					row_id  = outlet.id
					out_dict["id"] = outlet.id
					out_dict["company_logo"] = \
					Media_Path+str(outlet.Company.company_logo)
					out_dict["Outletname"] = outlet.Outletname
					out_dict["address"] = outlet.address
					if outlet.gst == None:
						gst = "N/A"
					else:
						gst = outlet.gst
					out_dict["address"] = out_dict["address"]+" GST: "+gst
					out_dict["temp_detail"] = []
					temp_record = TempTracking.objects.filter(outlet=row_id,created_at__date=today,is_latest=1).\
														order_by('-created_at')
					if temp_record.count() == 0:
						out_dict['time_stamp'] = None
					else:
						for j in temp_record:
							data_dict = {}
							data_dict['staff_id'] = j.staff_id
							data_dict['staff_name'] = j.staff.manager_name
							data_dict['body_temp'] = j.body_temp
							data_dict['spo2'] = j.SPO2
							out_dict["temp_detail"].append(data_dict)
						t = j.created_at+timedelta(hours=5,minutes=30)
						out_dict["time_stamp"] = t.strftime("%Y-%m-%d %I:%M %p")
					final_result.append(out_dict)
			return Response({
							"success"	:	True,
							"message"	:	"API worked well!!",
							"data"		:	final_result
							 })
		except Exception as e:
			return Response({
				"success"	: 	False, 
				"message"	: 	"Error happened!!", 
				"errors"	: 	str(e)
				})



			



