import os
from _thread import start_new_thread

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from Orders.models import Order
import dateutil.parser

from reports.models import Report, ReportErrorGenerator
from .product_level_report import result_data
import xlwt
from django.http import HttpResponse
from ZapioApi.Api.download_token import token_create, token_delete
from UserRole.models import DownloadToken
from datetime import datetime,timedelta

from ZapioApi.Api.BrandApi.ordermgmt.csv_order import Reportsvaidation, correct_response


def reportscsv(s_date,e_date,data,outletss,user_id):
	try:
		start_date = dateutil.parser.parse(str(s_date)).date()
		end_date = dateutil.parser.parse(str(e_date)).date()
		if bool(data['is_all']) == False:
			order_record = Order.objects.filter(order_time__date__gte=start_date, \
												order_time__date__lte=end_date, \
												outlet=outletss)
		else:
			order_record = Order.objects.filter(order_time__date__gte=start_date, \
												order_time__date__lte=end_date)
		to_proceed = 1
		if order_record.count() != 0:
			if bool(data['is_all']) == False:
				report_outlet_name = order_record[0].outlet.Outletname
			else:
				report_outlet_name = "ALL OUTLETS"
		else:
			to_proceed = 0


		if to_proceed == 1:
			result = result_data(order_record)
			wb = xlwt.Workbook()
			ws = wb.add_sheet("ProductLevelReport")

			row_num = 0

			columns = [

				("S.No", 2000),
				("Final Product Id", 3000),
				# ("outlet_name", 2000),
				("Product" ,5000),
				("Variant", 4000),
				("Total Orders", 2000),
				("Average Rating", 2000),
				("Total Rating", 2000),
				("Total Rated Orders", 5000),

			]

			font_style = xlwt.XFStyle()
			font_style.font.bold = True

			for col_num in range(len(columns)):
				ws.write(row_num, col_num, columns[col_num][0], font_style)
				# set column width
				ws.col(col_num).width = columns[col_num][1]

			font_style = xlwt.XFStyle()
			font_style.alignment.wrap = 1
			for i in result:
				row_num += 1
				row = [
					row_num,
					int(i["final_product_id"]),
					# i["outlet_name"],
					i["product_name"],
					i["variant"],
					i["order_count"],
					i["avg_rating"],
					i["total_rating"],
					i["rated_order"],

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
			report_name = "ProductLevelReport " +report_outlet_name+" "+str(start_date) + "-" + str(end_date)
			b = Report(auth_id_id=user_id, report_name=report_name, report=myfile, \
					   file_size=im_size, created_at=datetime.now())
			b.save()
			os.remove(file_name)
		else:
			pass
		return None
	except Exception as e:
		error_create = ReportErrorGenerator.objects.create(error_report=str(e))
		return "error_occured"


class ProductLevelCSV(APIView):
	"""
	Product Level Report  data POST API

			Authentication Required		: Yes
			Service Usage & Description	: Product level csv file request for dropbox

			Data Post:{

				"is_all"		: 	""(True or False)
				"start_date"	: 	"2020-08-15",
				"end_date"		: 	"2020-08-17",
				"outlet_ids"	: 	"18",

			}
		
			Response: {

				"success"	: 	True,
				"message"	: 	"Request has been queued...check dropbox after some time!!"
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
			is_all = data['is_all']
			if is_all != True and is_all != False:
				err_message['is_all'] = "Flag is not set properly!!"
			else:
				pass
			try:
				start_date = dateutil.parser.parse(s_date)
				end_date = dateutil.parser.parse(e_date)
				if start_date < end_date:
					pass
				else:
					err_message["date"] = "Please provide meaning full date range!!"
			except Exception as e:
				err_message["date"] = "Please provide meaning full date range!!"
			if is_all == False:
				try:
					data["outlet_ids"] = int(data["outlet_ids"])
				except Exception as e:
					err_message["outlet"] = "Outlet is not valid!!"
			else:
				pass
			if any(err_message.values())==True:
					return Response({
						"success"	: 	False,
						"error" 	: 	err_message,
						"message" 	: 	"Please correct listed errors!!"

						})
			report_record = Report.objects.filter(auth_id=user_id)
			total_reports = \
				report_record.aggregate(Sum('file_size'))['file_size__sum'] or 0
			if total_reports <100:
				pass
			else:
				err_message["dropbox"] = "Please delete some reports from your dropbox to "+ \
										 " generate new one!!"
				return Response({
					"success"	: 	False,
					"error" 	: 	err_message,
					"message" 	: 	"Please correct listed errors!!"
				})
			if is_all == False:
				outletss = data["outlet_ids"]
				start_new_thread(reportscsv, (s_date, e_date,data, outletss, user_id))
				response = correct_response()
			else:
				outletss = None
				start_new_thread(reportscsv, (s_date, e_date,data,outletss, user_id))
				response = correct_response()
			return response
		except Exception as e:
			return Response({
			"succes"	: 	False,
			"messag"	: 	"Error happened!!",
			"error"		: 	str(e)
			})


