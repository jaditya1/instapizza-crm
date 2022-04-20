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
from Product.models import Product,ProductCategory,Variant
from rest_framework.authtoken.models import Token
from UserRole.models import ManagerProfile
from ZapioApi.Api.BrandApi.ordermgmt.csv_order import Reportsvaidation, correct_response
from reports.models import Report, ReportErrorGenerator


def reportscsv(s_date,e_date,outletss,user_id):
	try:
		user = user_id
		datas = Order.objects.filter(Q(order_time__lte=e_date), Q(order_time__gte=s_date)).order_by('-order_time')
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
			("id", 3000),
			("Add On Name", 3000),
			("Sold Quantity", 3000),
			("Price", 3000),
			("Outlet", 3000),
			("Invoice No", 3000),
			("Source", 3000),
			("Order_Date", 3000),
			("Order_Time", 3000),
			("Is canceled", 3000),
		]
		font_style = xlwt.XFStyle()
		font_style.font.bold = True
		for col_num in range(len(columns)):
			ws.write(row_num, col_num, columns[col_num][0], font_style)
			ws.col(col_num).width = columns[col_num][1]
		font_style = xlwt.XFStyle()
		font_style.alignment.wrap = 1
		ord_data = []
		ord_data1 = []
		ord_data3 = []
		for k in outletss:
			data = datas.filter(outlet_id=k)
			q_count = data.count()
			if q_count > 0:
				for i in data:
					if i.is_aggregator == True:
						if i.order_description != None:
							for j in i.order_description:
								if 'add_ons' in j:
									k = j['add_ons']
									for p in k:
										alls = {}
										price = p['price']
										if 'addon_name' in p:
											alls['addon_name'] = p['addon_name']
										else:
											pass
										if 'final_addon_id' in p:
											alls['id'] = p['final_addon_id']
										else:
											pass
										if 'title' in p:
											alls['addon_name'] = p['title']
										else:
											pass
										if 'quantity' in p:
											alls['quantity'] = p['quantity']
										else:
											alls['quantity'] = j['quantity']
										alls['order_id'] = i.outlet_order_id
										alls['price'] = p['price']
										alls['source'] = i.payment_source
										chk_cancel = i.order_status_id
										if str(chk_cancel) == str(7):
											alls['c_canel'] = 'Yes'
										else:
											alls['c_canel'] = 'No'
										o = i.order_time
										o_time = o + timedelta(hours=5, minutes=30)
										alls['time'] = o_time.time()
										alls['dt'] = o_time.date()
										alls['outlet'] = OutletProfile.objects.filter(id=i.outlet_id)[0].Outletname
										ord_data.append(alls)
								else:
									pass
						else:
							pass
					else:
						if i.order_description != None:
							for j in i.order_description:
								if 'add_ons' in j:
									k = j['add_ons']
									for p in k:
										alls = {}
										price = p['price']
										if 'addon_name' in p:
											alls['addon_name'] = p['addon_name']
										else:
											pass
										if 'add_on_id' in p:
											alls['id'] = p['add_on_id']
										else:
											pass
										if 'addon_id' in p:
											alls['id'] = p['addon_id']
										else:
											pass
										if 'title' in p:
											alls['addon_name'] = p['title']
										else:
											pass
										if 'quantity' in p:
											alls['quantity'] = p['quantity']
										else:
											alls['quantity'] = 1
										alls['order_id'] = i.outlet_order_id
										alls['price'] = p['price']
										alls['source'] = i.payment_source
										chk_cancel = i.order_status_id
										if str(chk_cancel) == str(7):
											alls['c_canel'] = 'Yes'
										else:
											alls['c_canel'] = 'No'
										o = i.order_time
										o_time = o + timedelta(hours=5, minutes=30)
										# alls['time'] = str(o_time.strftime("%I:%M %p"))
										alls['time'] = o_time.time()
										# alls['dt'] = str(o_time.strftime("%d/%b/%y"))
										alls['dt'] = o_time.date()
										alls['outlet'] = OutletProfile.objects.filter(id=i.outlet_id)[0].Outletname
										ord_data1.append(alls)
								else:
									pass
						else:
							pass
			else:
				pass

		ord_data3 = ord_data + ord_data1
		for obj in ord_data3:
			if 'order_id' in obj:
				order_id = obj['order_id']
			else:
				order_id = 'N/A'
			if 'addon_name' in obj:
				addon_name = obj['addon_name']
			else:
				addon_name = 'N/A'
			if 'id' in obj:
				ids = obj['id']
			else:
				ids = 'N/A'
			if 'quantity' in obj:
				quantity = obj['quantity']
			else:
				quantity = 'N/A'
			if 'price' in obj:
				price = obj['price']
			else:
				price = 'N/A'
			if 'source' in obj:
				source = obj['source']
			else:
				source = 'N/A'
			if 'outlet' in obj:
				outlet_name = obj['outlet']
			else:
				outlet_name = 'N/A'
			t = obj['time']
			d = obj['dt']
			canc = obj['c_canel']
			row_num += 1
			row = [
				ids,
				addon_name,
				quantity,
				price,
				outlet_name,
				order_id,
				source,
				d,
				t,
				canc
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
		report_name = "AddonReport " + str(start_date) + "-" + str(end_date)
		b = Report(auth_id_id=user_id, report_name=report_name, report=myfile, \
				   file_size=im_size, created_at=datetime.now())
		b.save()
		os.remove(file_name)
		return None
	except Exception as e:
		error_create = ReportErrorGenerator.objects.create(error_report=str(e))
		return "error_occured"

class AddonReportCsv(APIView):
	"""
	Addon Report data POST API

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
			"succes"	: 	False,
			"messag"	: 	"Error happened!!",
			"error"		: 	str(e)
			})


