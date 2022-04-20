from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile,TempTracking
import re
from ZapioApi.api_packages import *
from datetime import datetime, timedelta


class ALLOutlets(APIView):
	"""
	Active Outlets Stream listing GET API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to get listing of Active Outlets along with cam url.

	"""
	def get(self, request, format=None):
		try:
			check_company = OutletProfile.objects.filter(Company_id=1,active_status=1).order_by('priority')
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
					if row_id != 35 and row_id != 34 and row_id != 33:
						out_dict["id"] = outlet.id
						out_dict["Outletname"] = outlet.Outletname
						if row_id != 26 and row_id != 32:
							out_dict["is_open"] = outlet.is_pos_open
							out_dict["cam_url"] = outlet.cam_url
						else:
							out_dict["is_open"] =  False
							out_dict["cam_url"] = None
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
						out_dict["priority"] = outlet.priority
						final_result.append(out_dict)
					else:
						pass
			return Response({
							"success"	:	True,
							"message"	:	"Active Outlets stream listing worked well!!",
							"data"		:	final_result
							 })
		except Exception as e:
			print("Active Outlets stream listing Api Stucked into exception!!")
			print(e)
			return Response({
					"success": False, 
					"message": "Error happened!!", 
					"errors": str(e)
					})
