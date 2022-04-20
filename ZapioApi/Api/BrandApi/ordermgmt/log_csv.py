import os
from _thread import start_new_thread
from datetime import datetime
import requests
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework import serializers
from django.http import HttpResponse
from Orders.models import Order,OrderStatusType,OrderTracking
from rest_framework.permissions import IsAuthenticated
import dateutil.parser
from Brands.models import Company
from Outlet.models import *
from rest_framework.authtoken.models import Token
from UserRole.models import ManagerProfile
from datetime import datetime, timedelta
from History.models import OutletLogs
from ZapioApi.Api.BrandApi.ordermgmt.csv_order import Reportsvaidation, correct_response
from reports.models import Report, ReportErrorGenerator


def reportscsv(s_date,e_date,outletss,user_id):
	try:
		user = user_id
		import xlwt

		wb = xlwt.Workbook()
		ws = wb.add_sheet("outlet_log")
		row_num = 0
		columns = [
			("Order & Invoice Details", 10000),
			("Order Value Details", 10000),
		]
		font_style = xlwt.XFStyle()
		font_style.font.bold = True
		pattern = xlwt.Pattern()
		pattern.pattern = xlwt.Pattern.SOLID_PATTERN
		pattern.pattern_fore_colour = xlwt.Style.colour_map['black']  # Set the cell background color to yellow
		font_style.pattern = pattern
		font_style.alignment.wrap = 1
		row_num = 0
		columns = [
			("OUTLET NAME", 3000),
			("DATE", 3000),
			("OPENING TIME", 3000),
			("CLOSING TIME", 3000),
			("STATUS", 3000),
			("RESPONSE USER", 3000),
		]
		for col_num in range(len(columns)):
			ws.write(row_num, col_num, columns[col_num][0], font_style)
			ws.col(col_num).width = columns[col_num][1]
		font_style = xlwt.XFStyle()
		font_style.alignment.wrap = 1
		query = OutletLogs.objects.filter(Q(created_at__lte=e_date), Q(created_at__gte=s_date))
		q_count = query.count()
		if q_count > 0:
			ord_data = []
			for k in outletss:
				logdata = query.filter(outlet_id=k)
				for i in logdata:
					p_list = {}
					if i.opening_time != None:
						o_time = i.opening_time + timedelta(hours=5, minutes=30)
						ot = str(o_time.time())
						s = ot.split('.')
						p_list['opening_time'] = s[0]
					else:
						p_list['opening_time'] = ''
					if i.closing_time != None:
						o_time = i.closing_time + timedelta(hours=5, minutes=30)
						ot = str(o_time.time())
						s = ot.split('.')
						p_list['closing_time'] = s[0]
					else:
						p_list['closing_time'] = ''
					if i.created_at != None:
						c_time = i.created_at + timedelta(hours=5, minutes=30)
						p_list['created_at'] = c_time.strftime("%Y-%m-%d")
					else:
						p_list['created_at'] = ''
					p_list['outlet'] = i.outlet.Outletname
					cid = ManagerProfile.objects.filter(auth_user_id=i.auth_user)
					p_list['user'] = cid[0].username
					st = i.is_open
					if st == True:
						p_list['status'] = 'Open'
					else:
						p_list['status'] = 'Closed'
					ord_data.append(p_list)
		else:
			ord_data = []
		for obj in ord_data:
			oname = obj['outlet']
			dt = obj['created_at']
			otime = obj['opening_time']
			ctime = obj['closing_time']
			st = obj['status']
			user = obj['user']
			row_num += 1
			row = [
				oname,
				dt,
				otime,
				ctime,
				st,
				user
			]
			for col_num in range(len(row)):
				ws.write(row_num, col_num, row[col_num], font_style)
		import secrets
		a = secrets.token_hex(10)
		file_name = 'Report' + a + '.xls'
		wb.save(file_name)
		from django.core.files import File
		f = open(file_name, 'rb')
		myfile = File(f)

		im_name_path = myfile.file.name
		im_size = (os.stat(im_name_path).st_size) / 1024 / 1024
		start_date = dateutil.parser.parse(str(s_date)).date()
		end_date = dateutil.parser.parse(str(e_date)).date()
		report_name = "OutletLogReport" + str(start_date) + "-" + str(end_date)
		b = Report(auth_id_id=user_id, report_name=report_name, report=myfile, file_size=im_size, created_at=datetime.now())
		b.save()
		os.remove(file_name)
		return None
	except Exception as e:
		error_create = ReportErrorGenerator.objects.create(error_report=str(e))
		return "error_occured"

class AllLogCsv(APIView):
	"""
	Outlet log data POST API

		Authentication Required			: 	Yes
		Service Usage & Description		: 	This service is used to place a report request to be generated.

		Data Post: {

    		"outlet_ids"    : 	["18","10"],
   			"start_date"    :   "2020-07-15",
    		"end_date"      :   "2020-08-17"
		}

		Response: {

			"success"	 :	True,
			"message"	 : 'Request has been queued...check dropbox after some time!!'
		}

		"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			err_message = {}
			user_id = request.user.id
			s_date = data['start_date']
			e_date = data['end_date']
			err_response = Reportsvaidation(s_date,e_date,data,err_message,user_id)
			if err_response == None:
				pass
			else:
				return err_response
			start_new_thread(reportscsv,(s_date,e_date,data["outlet_ids"],user_id))
			response = correct_response()
			return response
		except Exception as e:
			return Response({
				"succes": False,
				"messag": "Error happened!!",
				"error"	: 	str(e)
			})

