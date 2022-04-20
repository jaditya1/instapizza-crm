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
from Orders.models import Order,OrderStatusType
from rest_framework.permissions import IsAuthenticated
import dateutil.parser
from Brands.models import Company
from Outlet.models import OutletProfile
from datetime import datetime, timedelta

from datetime import datetime, timedelta
from Product.models import Product,ProductCategory,Variant,Addons,AddonDetails
from ZapioApi.Api.BrandApi.ordermgmt.csv_order import Reportsvaidation
from reports.models import Report, ReportErrorGenerator


def reportscsv(s_date,e_date,outletss,user_id):
	try:
		data = Addons.objects.filter(Company_id=1)
		import xlwt
		wb = xlwt.Workbook()
		ws = wb.add_sheet("addon_reports")
		row_num = 0
		columns = [
			("Order & Invoice Details", 10000),
			("Order Value Details", 10000),
		]
		font_style = xlwt.XFStyle()
		font_style.font.bold = True
		pattern = xlwt.Pattern()
		pattern.pattern = xlwt.Pattern.SOLID_PATTERN
		pattern.pattern_fore_colour = xlwt.Style.colour_map['blue']  # Set the cell background color to yellow
		font_style.pattern = pattern
		font_style = xlwt.XFStyle()
		font_style.alignment.wrap = 1
		date_format = xlwt.XFStyle()
		date_format.num_format_str = 'dd/mm/yyyy'
		row_num = 0

		columns = [
			("ID", 3000),
			("Addon Name", 3000),
			("Addon Price", 3000),
			("Addon Group Name", 3000),
			("Addon Group Status", 3000),
			("Addon Group Id", 3000),
			("Varient Name", 3000),
			("Varient ID", 3000)
		]

		font_style = xlwt.XFStyle()
		font_style.font.bold = True
		for col_num in range(len(columns)):
			ws.write(row_num, col_num, columns[col_num][0], font_style)
			ws.col(col_num).width = columns[col_num][1]

		font_style = xlwt.XFStyle()
		font_style.alignment.wrap = 1

		q_count = data.count()
		print(q_count)
		ord_data = []
		if q_count > 0:
			for i in data:
				alls = {}

				a = i.name
				if a in ord_data:
					pass
				else:
					alls['id'] = i.id
					alls['name'] = i.name
					alls['price'] = i.addon_amount
					alls['gr'] = i.addon_group_id
				ord_data.append(alls)

		# print("hhhhhhhhhhhhhhhhhhhhhh",ord_data)
		for obj in ord_data:
			print(obj)			# {'id': 719, 'name': 'test', 'price': 2.0, 'gr': None}
			row_num += 1
			addon_group_name = AddonDetails.objects.filter(id=str(obj['gr']))[0].addon_gr_name
			st = AddonDetails.objects.filter(id=str(obj['gr']))[0].active_status
			v = AddonDetails.objects.filter(id=str(obj['gr']))[0].product_variant_id
			vn = Variant.objects.filter(id=v)
			if vn.count() > 0:
				a = vn[0].id
				b = vn[0].variant
			else:
				b = 'N/A'
				a = 'N/A'
			if st == 0:
				s = "Inactive"
			else:
				s = "Active"
			row = [
				obj['id'],
				obj['name'],
				obj['price'],
				addon_group_name,
				s,
				str(obj['gr']),
				b,
				a
			]
			# print(row)
			for col_num in range(len(row)):
				ws.write(row_num, col_num, row[col_num], font_style)
		import secrets
		a = secrets.token_hex(10)
		file_name = 'Report'+a+'.xls'
		wb.save(file_name)
		from django.core.files import File
		f = open(file_name,'rb')
		myfile = File(f)
		im_name_path = myfile.file.name
		im_size = (os.stat(im_name_path).st_size)/1024/1024
		start_date = dateutil.parser.parse(str(s_date)).date()
		end_date = dateutil.parser.parse(str(e_date)).date()
		report_name = "addon_reports "+str(start_date)+"-"+str(end_date)
		b = Report(auth_id_id = user_id,report_name=report_name,report=myfile,\
								file_size = im_size,created_at = datetime.now())
		b.save()
		os.remove(file_name)

		return None
	except Exception as e:
		error_create = ReportErrorGenerator.objects.create(error_report=str(e))
		return "error_occured"


class Addoncsv(APIView):
	"""
        Addon Report  data GET API

            Authentication Required		: Yes
            Service Usage & Description	: .Download Product csv file

            Data Post:
            {
             	"outlet_ids"    : 	["18","10"],
	   			"start_date"    :   "2020-07-15",
	    		"end_date"      :   "2020-08-17"
			}


            Response: {

                "success": True,
                "message": "Request has been queued...check dropbox after some time!!"
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
			outletss = data["outlet_ids"]
			response = Reportsvaidation(s_date,e_date,data,err_message,user_id)
			start_new_thread(reportscsv, (s_date, e_date, outletss, user_id))
			return response
		except Exception as e:
			return Response({
			"succes"	: 	False,
			"messag"	: 	"Error happened!!",
			"error"		: 	str(e)
			})

