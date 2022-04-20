import os
from _thread import start_new_thread
# from _dummy_thread import start_new_thread
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
from Outlet.models import OutletProfile
from rest_framework.authtoken.models import Token
from UserRole.models import ManagerProfile

from datetime import datetime, timedelta
from django.db.models import Count, Sum, Max, Avg, Case, When, Value, IntegerField, BooleanField

from ZapioApi.Api.BrandApi.ordermgmt.csv_order import Reportsvaidation, correct_response
from reports.models import Report, ReportErrorGenerator


def reportscsv(s_date,e_date,outletss,user_id):
	try:
		import xlwt
		wb = xlwt.Workbook()
		ws = wb.add_sheet("payment_report")
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
			("Outlet", 3000),
			("Orders", 3000),
			("COD", 3000),
			("COD ORDERS", 3000),
			("DINEOUT", 3000),
			("DINEOUT ORDERS", 3000),
			("PAYTM", 3000),
			("PAYTM ORDERS", 3000),
			("RAZORPAY", 3000),
			("RAZORPAT_ORDERS", 3000),
			("PAYU", 3000),
			("PAYU_ORDERS", 3000),
			("EDC", 3000),
			("EDC ORDERS", 3000),
			("MOBIQUIK", 3000),
			("MOBIQUIK ORDERS", 3000),
			("EDC_AMEX", 3000),
			("EDC_AMEX ORDERS", 3000),
			("EDC_YES_BANK", 3000),
			("EDC_YES_BANK ORDERS", 3000),
			("SWIGGY ONLINE", 3000),
			("SWIGGY ONLINE ORDERS", 3000),
			("Z0MATO ONLINE", 3000),
			("Z0MATO ONLINE ORDERS", 3000),
			("TOTAL ORDERS AMOUNT", 3000),
		]

		font_style = xlwt.XFStyle()
		font_style.font.bold = True
		for col_num in range(len(columns)):
			ws.write(row_num, col_num, columns[col_num][0], font_style)
			ws.col(col_num).width = columns[col_num][1]
		font_style = xlwt.XFStyle()
		font_style.alignment.wrap = 1
		# outlet = outlet
		orderdata = []
		end_date = e_date
		start_date = s_date
		que = Order.objects.filter(Q(order_time__lte=end_date), Q(order_time__gte=start_date))
		orderdata = []
		for j in outletss:
			query = que.filter(outlet_id=j)
			if query.count() > 0:
				for i in query:
					adata = {}
					cname = i.Company.company_name
					adata['outlet_id'] = i.outlet_id
					adata['id'] = i.id
					if i.outlet_id != None:
						outlet_name = OutletProfile.objects.filter(id=i.outlet_id)[0].Outletname
						adata['outlet_name'] = str(cname) + ' ' + str(outlet_name)
					else:
						pass
					pdetail = Order.objects.filter(Q(order_time__lte=end_date), \
												   Q(order_time__gte=start_date), \
												   Q(outlet_id=i.outlet_id))

					adata['cod'] = 0
					adata['cod_count'] = 0
					adata['Dineout'] = 0
					adata['Dineout_count'] = 0
					adata['Paytm'] = 0
					adata['Paytm_count'] = 0
					adata['Razorpay'] = 0
					adata['Razorpay_count'] = 0
					adata['PayU'] = 0
					adata['PayU_count'] = 0
					adata['EDC'] = 0
					adata['EDC_count'] = 0
					adata['Mobiquik'] = 0
					adata['Mobiquik_count'] = 0
					adata['mix'] = 0
					adata['Amex'] = 0
					adata['Amex_count'] = 0
					adata['yes'] = 0
					adata['yes_count'] = 0
					adata['total_amount'] = 0
					adata['order_count'] = 0
					for j in pdetail:
						if j.settlement_details != None:
							if len(j.settlement_details) > 0:
								k = 1
								for k in j.settlement_details:
									if k['mode'] == 0:
										c = k['amount']
										adata['cod'] = adata['cod'] + float(c)
										adata['cod_count'] = adata['cod_count'] + 1
									else:
										pass
									if k['mode'] == 1:
										d = k['amount']
										adata['Dineout'] = adata['Dineout'] + float(d)
										adata['Dineout_count'] = adata['Dineout_count'] + 1
									else:
										pass
									if k['mode'] == 2:
										p = k['amount']
										adata['Paytm'] = adata['Paytm'] + float(p)
										adata['Paytm_count'] = adata['Paytm_count'] + 1
									else:
										pass
									if k['mode'] == 3:
										r = k['amount']
										adata['Razorpay'] = adata['Razorpay'] + float(r)
										adata['Razorpay_count'] = adata['Razorpay_count'] + 1
									else:
										pass
									if k['mode'] == 4:
										p = k['amount']
										adata['PayU'] = adata['PayU'] + float(p)
										adata['PayU_count'] = adata['PayU_count'] + 1
									else:
										pass
									if k['mode'] == 5:
										e = k['amount']
										adata['EDC'] = adata['EDC'] + float(e)
										adata['EDC_count'] = adata['EDC_count'] + 1
									else:
										pass
									if k['mode'] == 6:
										m = k['amount']
										adata['Mobiquik'] = adata['Mobiquik'] + float(m)
										adata['Mobiquik_count'] = adata['Mobiquik_count'] + 1
									else:
										pass
									if k['mode'] == 7:
										mix = k['amount']
									else:
										pass
									if k['mode'] == 8:
										a = k['amount']
										adata['Amex'] = adata['Amex'] + float(a)
										adata['Amex_count'] = adata['Amex_count'] + 1
									else:
										pass
									if k['mode'] == 9:
										y = k['amount']
										adata['yes'] = adata['yes'] + float(y)
										adata['yes_count'] = adata['yes_count'] + 1
									else:
										pass
								adata['total_amount'] = adata['Razorpay'] + \
														adata['Paytm'] + \
														adata['cod'] + \
														adata['EDC'] + \
														adata['Dineout'] + \
														adata['PayU'] + \
														adata['yes'] + \
														adata['Amex'] + \
														adata['Mobiquik']
								adata['order_count'] = adata['Razorpay_count'] + \
													   adata['Paytm_count'] + \
													   adata['cod_count'] + \
													   adata['EDC_count'] + \
													   adata['Dineout_count'] + \
													   adata['PayU_count'] + \
													   adata['yes_count'] + \
													   adata['Amex_count'] + \
													   adata['Mobiquik_count']

					orderdata.append(adata)
			else:
				pass

		for i in orderdata:
			Orders = i['order_count']
			cod = i['cod']
			cod_orders = i['cod_count']
			dineout = i['Dineout']
			dineout_orders = i['Dineout_count']
			paytm = i['Paytm']
			paytm_orders = i['Paytm_count']
			razorpay = i['Razorpay']
			razorpay_orders = i['Razorpay_count']
			payU = i['PayU']
			payU_orders = i['PayU_count']
			edc = i['EDC']
			edc_orders = i['EDC_count']
			mobiquik = i['Mobiquik']
			mobiquik_orders = i['Mobiquik_count']
			amex = i['Amex']
			amex_orders = i['Amex_count']
			yes = i['yes']
			yes_orders = i['yes_count']
			total_amount = i['total_amount']
			sn = 0
			sno = 0
			zo = 0
			zoo = 0
			row_num += 1
			row = [
				i['outlet_name'],
				Orders,
				cod,
				cod_orders,
				dineout,
				dineout_orders,
				paytm,
				paytm_orders,
				razorpay,
				razorpay_orders,
				payU,
				payU_orders,
				edc,
				edc_orders,
				mobiquik,
				mobiquik_orders,
				amex,
				amex_orders,
				yes,
				yes_orders,
				sn,
				sno,
				zo,
				zoo,
				total_amount

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
		start_date = dateutil.parser.parse(str(start_date)).date()
		end_date = dateutil.parser.parse(str(end_date)).date()
		report_name = "PaymentReport " + str(start_date) + "-" + str(end_date)
		b = Report(auth_id_id=user_id, report_name=report_name, report=myfile, \
				   file_size=im_size, created_at=datetime.now())
		b.save()
		os.remove(file_name)
		return None
	except Exception as e:
		error_create = ReportErrorGenerator.objects.create(error_report=str(e))
		return "error_occured"

class PaymentReportCsv(LoggingMixin,APIView):

	"""
	Payment Report data POST API

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
			s_date = dateutil.parser.parse(s_date)
			e_date = dateutil.parser.parse(e_date)
			start_new_thread(reportscsv,(s_date,e_date,data["outlet_ids"],user_id))
			response = correct_response()
			return response
		except Exception as e:
			return Response({
			"succes"	: 	False,
			"message"	: 	"Error happened!!",
			"error"		: 	str(e)
			})




