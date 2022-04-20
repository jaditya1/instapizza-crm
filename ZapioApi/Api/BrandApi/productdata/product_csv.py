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
from Orders.models import Order,OrderStatusType,OrderTracking, OrderProcessTimeLog
from rest_framework.permissions import IsAuthenticated
import dateutil.parser
from Brands.models import Company
from Outlet.models import OutletProfile
from rest_framework.authtoken.models import Token
from UserRole.models import ManagerProfile

from datetime import datetime, timedelta
from Product.models import Product,ProductCategory,Variant
from ZapioApi.Api.BrandApi.ordermgmt.csv_order import Reportsvaidation, correct_response
from reports.models import Report, ReportErrorGenerator
from urbanpiper.models import *

def floatconverter(data):
	try:
		data = float(data)
	except Exception as e:
		data = 0
	return data

def reportscsv(s_date,e_date,outletss,user_id):
	try:
		user = user_id
		end_date = e_date
		start_date = s_date
		datas = \
			Order.objects.filter(Q(order_time__lte=end_date), \
								 Q(order_time__gte=start_date)).order_by('-order_time')
		import xlwt

		wb = xlwt.Workbook()
		ws = wb.add_sheet("product_reports")
		row_num = 0
		columns = [
			("Product & Invoice Details", 12000),
			("Order Metrics Details", 10000),
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
			("Product id", 3000),
			("Product Name", 3000),
			("Price", 3000),
			("quantity", 3000),
			("Total Price", 3000),
			("Category", 3000),
			("Outlet", 3000),
			("Invoice No", 3000),
			("Source", 3000),
			("Order_Date", 3000),
			("Order_Time", 3000),
			("Is canceled", 3000),
			("Food Ready", 3000),
			("Discount", 3000),
			("Order_Value_Pre_tax#", 3000),
			("CGST %", 3000),
			("CGST Value", 3000),
			("SGST %", 3000),
			("SGST Value", 3000),
			("CESS %", 3000),
			("CESS Value", 3000),
			("Total Tax", 3000),
			("Order_Value_Post-Tax", 3000),
			("Short & Excess_Round Off", 3000),
			("Total_Bill_Value", 3000),
			("Payment Mode", 3000),
			("Order Rating", 3000),
			("Acceptance Time", 3000),
			("Food Ready Time", 3000),
			("KPT To Dispatch Time", 3000),
			("TTK", 3000)
		]

		font_style = xlwt.XFStyle()
		font_style.font.bold = True
		for col_num in range(len(columns)):
			ws.write(row_num, col_num, columns[col_num][0], font_style)
			ws.col(col_num).width = columns[col_num][1]

		font_style = xlwt.XFStyle()
		font_style.alignment.wrap = 1
		ord_data = []
		for k in outletss:
			data = datas.filter(outlet_id=k)
			q_count = data.count()
			if q_count > 0:
				for i in data:
					p_list = {}
					if i.is_aggregator == True:
						if i.order_description != None:
							for j in i.order_description:
								alls = {}
								process_log_record = \
									OrderProcessTimeLog.objects.filter(order=i.id)
								if i.rating != None and i.rating != "":
									alls["rating"] = i.rating
								else:
									alls["rating"] = "N/A"
								if process_log_record.count() == 1:
									process_q = process_log_record[0]
									alls["acceptance_time"] = process_q.order_acceptance_time
									alls["food_ready_time"] = process_q.kpt
									alls["kpt_to_dispatch"] = process_q.kpt_to_dispatch
									alls["ttk"] = \
										(alls["acceptance_time"] + alls["food_ready_time"] + \
										 alls["kpt_to_dispatch"])
								else:
									alls["acceptance_time"] = "N/A"
									alls["food_ready_time"] = "N/A"
									alls["kpt_to_dispatch"] = "N/A"
									alls["ttk"] = "N/A"
								alls['order_id'] = i.order_id
								alls['source'] = i.order_source
								alls['invoice'] = i.outlet_order_id
								chk_cancel = i.order_status_id
								if str(chk_cancel) == str(7):
									alls['c_canel'] = 'Yes'
								else:
									alls['c_canel'] = 'No'
								track_chk = OrderTracking.objects.filter(Q(order_id=i.id), \
																		 Q(Order_staus_name_id=3))
								if track_chk.count() > 0:
									alls['food_ready'] = 'Yes'
								else:
									alls['food_ready'] = 'No'
								if 'discount_amount' in j:
									alls['product_discount'] = j['discount_amount']
								else:
									alls['product_discount'] = 0
								if 'tax_detail' in j:
									tax_detail = j['tax_detail']
									if len(tax_detail) > 0:
										cgst = tax_detail[0]['tax_name']
										alls['cgst_percent'] = tax_detail[0]['tax_percent']
										if 'tax_value' in tax_detail[0]:
											alls['cgst_value'] = tax_detail[0]['tax_value']
										else:
											alls['cgst_value'] = 0
									else:
										alls['cgst_value'] = 0
										alls['cgst_value'] = 0

									if len(tax_detail) > 1:
										sgst = tax_detail[1]['tax_name']
										alls['sgst_percent'] = tax_detail[1]['tax_percent']
										if 'tax_value' in tax_detail[1]:
											alls['sgst_value'] = tax_detail[1]['tax_value']
										else:
											alls['sgst_value'] = 0
									else:
										alls['sgst_percent'] = 0
										alls['sgst_value'] = 0

									if len(tax_detail) > 2:
										cess = tax_detail[2]['tax_name']
										alls['cess_percent'] = tax_detail[2]['tax_percent']
										if 'tax_value' in tax_detail[2]:
											alls['cess_value'] = tax_detail[2]['tax_value']
										else:
											alls['cess_value'] = 0
									else:
										alls['cess_percent'] = 0
										alls['cess_value'] = 0
								else:
									alls['cgst_percent'] = 0
									alls['cgst_value'] = 0
									alls['sgst_percent'] = 0
									alls['sgst_value'] = 0
									alls['cess_percent'] = 0
									alls['cess_value'] = 0

								alls['total_tax'] = floatconverter(alls['cgst_value']) + floatconverter(alls['sgst_value']) + \
													floatconverter(alls['cess_value'])

								o_time = i.order_time + timedelta(hours=5, minutes=30)
								alls['time'] = o_time.time()
								alls['dt'] = o_time.date()
								if i.outlet_id != None:
									alls['outlet_name'] = OutletProfile.objects.filter(id=i.outlet_id)[0].Outletname
								else:
									alls['outlet_name'] = 'N/A'
								if 'name' in j:
									alls['name'] = j['name']
								else:
									alls['name'] = 'N/A'

								if 'product_id' in j:
									alls['ab'] = j['product_id']
								else:
									pass
								if 'final_product_id' in j:
									sp = ProductSync.objects.filter(id=j['final_product_id'])
									pid = sp[0].product_id
									if sp[0].variant_id != None:
										alls['vid'] = sp[0].variant_id
									else:
										alls['vid'] = ''

									a = Product.objects.filter(id=pid)
									alls['ab'] = j['final_product_id']
									if a.count() > 0:
										d = Product.objects.filter(id=pid)[0].product_category_id
										alls['category'] = ProductCategory.objects.filter(id=d)[0].category_name
									else:
										alls['category'] = 'N/A'
								else:
									alls['category'] = 'N/A'
									alls['ab'] = 'N/A'
								if 'food_type' in j:
									alls['food_type'] = j['food_type']
								else:
									alls['food_type'] = 'N/A'
								if 'varients' in j:
									if type(j['varients']) == str:
										alls['varients'] = j['varients']
									else:
										v = Variant.objects.filter(id=j['varients'])
										if v.count() > 0:
											alls['varients'] = v[0].variant
										else:
											alls['varients'] = ''
								else:
									alls['varients'] = ''
								if 'size' in j:
									alls['varients'] = j['size']
								else:
									alls['varients'] = ''
								if 'quantity' in j:
									alls['quantity'] = j['quantity']
								else:
									alls['quantity'] = 0
								alls['quantity'] = floatconverter(alls['quantity'])
								if 'price' in j:
									p = j['price']
									alls['price'] = round(p / alls['quantity'], 2)
								else:
									alls['price'] = 0
								alls['total_bill_value'] = floatconverter(alls['total_tax']) + floatconverter(alls['price'])
								alls["payment_mode"] = i.get_payment_mode_display()
								ord_data.append(alls)
					else:
						p_list['order_id'] = i.order_id
						p_list['product_detail'] = []
						if i.order_description != None:
							for j in i.order_description:
								alls = {}
								alls['order_id'] = i.order_id
								alls['source'] = i.order_source
								alls['invoice'] = i.outlet_order_id
								if i.rating != None and i.rating != "":
									alls["rating"] = i.rating
								else:
									alls["rating"] = "N/A"
								process_log_record = \
									OrderProcessTimeLog.objects.filter(order=i.id)
								if process_log_record.count() == 1:
									process_q = process_log_record[0]
									alls["acceptance_time"] = process_q.order_acceptance_time
									alls["food_ready_time"] = process_q.kpt
									alls["kpt_to_dispatch"] = process_q.kpt_to_dispatch
									alls["ttk"] = \
										(alls["acceptance_time"] + alls["food_ready_time"] + \
										 alls["kpt_to_dispatch"])
								else:
									alls["acceptance_time"] = "N/A"
									alls["food_ready_time"] = "N/A"
									alls["kpt_to_dispatch"] = "N/A"
									alls["ttk"] = "N/A"
								chk_cancel = i.order_status_id
								if str(chk_cancel) == str(7):
									alls['c_canel'] = 'Yes'
								else:
									alls['c_canel'] = 'No'
								track_chk = OrderTracking.objects.filter(Q(order_id=i.id), \
																		 Q(Order_staus_name_id=3))
								if track_chk.count() > 0:
									alls['food_ready'] = 'Yes'
								else:
									alls['food_ready'] = 'No'
								if 'tax_detail' in j:
									tax_detail = j['tax_detail']
									if len(tax_detail) > 0:
										cgst = tax_detail[0]['tax_name']
										alls['cgst_percent'] = tax_detail[0]['tax_percent']
										if 'tax_value' in tax_detail[0]:
											alls['cgst_value'] = tax_detail[0]['tax_value']
										else:
											alls['cgst_value'] = 0
									else:
										alls['cgst_percent'] = 0
										alls['cgst_value'] = 0

									if len(tax_detail) > 1:
										sgst = tax_detail[1]['tax_name']
										alls['sgst_percent'] = tax_detail[1]['tax_percent']
										if 'tax_value' in tax_detail[1]:
											alls['sgst_value'] = tax_detail[1]['tax_value']
										else:
											alls['sgst_value'] = 0
									else:
										alls['sgst_percent'] = 0
										alls['sgst_value'] = 0

									if len(tax_detail) > 2:
										cess = tax_detail[2]['tax_name']
										alls['cess_percent'] = tax_detail[2]['tax_percent']
										if 'tax_value' in tax_detail[2]:
											alls['cess_value'] = tax_detail[2]['tax_value']
										else:
											alls['cess_value'] = 0
									else:
										alls['cess_percent'] = 0
										alls['cess_value'] = 0
								else:
									alls['cgst_percent'] = 0
									alls['cgst_value'] = 0
									alls['sgst_percent'] = 0
									alls['sgst_value'] = 0
									alls['cess_percent'] = 0
									alls['cess_value'] = 0
								alls['total_tax'] = floatconverter(alls['cgst_value']) + floatconverter(alls['sgst_value']) + \
													floatconverter(alls['cess_value'])
								o_time = i.order_time + timedelta(hours=5, minutes=30)
								# alls['time'] = str(o_time.strftime("%I:%M %p"))
								alls['time'] = o_time.time()
								# alls['dt'] = str(o_time.strftime("%d/%b/%y"))
								alls['dt'] = o_time.date()
								if i.outlet_id != None:
									alls['outlet_name'] = OutletProfile.objects.filter(id=i.outlet_id)[0].Outletname
								else:
									alls['outlet_name'] = 'N/A'
								if 'name' in j:
									alls['name'] = j['name']
								else:
									alls['name'] = 'N/A'
								if 'product_id' in j:
									pid = j['product_id']
									d = Product.objects.filter(id=j['product_id'])[0].product_category_id
									alls['category'] = ProductCategory.objects.filter(id=d)[0].category_name
								else:
									pass
								if 'id' in j:
									pid = j['id']
									d = Product.objects.filter(id=j['id'])[0].product_category_id
									alls['category'] = ProductCategory.objects.filter(id=d)[0].category_name
								else:
									pass
								if 'price' in j:
									alls['price'] = j['price']
								else:
									alls['price'] = '0'
								alls['total_bill_value'] = floatconverter(alls['total_tax']) + floatconverter(alls['price'])

								if 'food_type' in j:
									alls['food_type'] = j['food_type']
								else:
									alls['food_type'] = 'N/A'
								if 'varients' in j:
									if type(j['varients']) == str:
										alls['varients'] = j['varients']
									else:
										v = Variant.objects.filter(id=j['varients'])
										if v.count() > 0:
											alls['varients'] = v[0].variant
											alls['vid'] = v[0].id

										else:
											alls['varients'] = ''
								else:
									alls['varients'] = ''
									alls['vid'] = ''
								if 'size' in j:
									alls['varients'] = j['size']
									if j['size'] != 'N/A':
										v = Variant.objects.filter(variant=j['size'])
										if v.count() > 0:
											alls['vid'] = v[0].id
										else:
											alls['vid'] = ''
								else:
									alls['varients'] = ''
									alls['vid'] = ''
								if alls['vid'] != '' and pid != '':
									sp = ProductSync.objects.filter(product_id=pid, variant_id=alls['vid'])
									if sp.count() > 0:
										alls['ab'] = sp[0].id
									else:
										alls['ab'] = ''
								else:
									alls['vid'] = ''
									sp = ProductSync.objects.filter(product_id=pid)
									if sp.count() > 0:
										alls['ab'] = sp[0].id
									else:
										alls['ab'] = ''
								if 'quantity' in j:
									alls['quantity'] = j['quantity']
									alls['cgst_value'] = \
									floatconverter(alls['cgst_value']) * floatconverter(j['quantity'])
									alls['sgst_value'] = \
									floatconverter(alls['sgst_value']) * floatconverter(j['quantity'])
									alls['cess_value'] = \
									floatconverter(alls['cess_value']) * floatconverter(j['quantity'])
									alls['total_tax'] = \
										alls['cgst_value'] + alls['sgst_value'] + alls['cess_value']
								else:
									alls['quantity'] = 0
								if 'discount_amount' in j:
									tdiscount = alls['quantity'] * j['discount_amount']
									alls['product_discount'] = tdiscount
								else:
									alls['product_discount'] = 0
								alls["payment_mode"] = i.get_payment_mode_display()
								ord_data.append(alls)
						else:
							pass
		for obj in ord_data:
			cgst_percent = obj['cgst_percent']
			cgst_value = obj['cgst_value']
			sgst_percent = obj['sgst_percent']
			sgst_value = obj['sgst_value']
			cess_percent = obj['cess_percent']
			cess_value = obj['cess_value']
			total_tax = obj['total_tax']
			vid = obj['vid']
			if 'order_id' in obj:
				order_id = obj['order_id']
			else:
				order_id = 'N/A'
			if 'source' in obj:
				source = obj['source']
				if source != None:
					source = obj['source']
				else:
					source = 'N/A'
			else:
				source = 'N/A'
			if 'name' in obj:
				name = obj['name']
			else:
				name = 'N/A'
			if 'food_type' in obj:
				food_type = obj['food_type']
			else:
				food_type = 'N/A'
			if 'price' in obj:
				price = floatconverter(obj['price'])
			else:
				price = 0
			if 'quantity' in obj:
				qty = obj['quantity']
			else:
				qty = 0
			if 'varients' in obj:
				varsss = obj['varients']
				if varsss == '':
					varss = ''
				else:
					varss = obj['varients']
			else:
				varss = ''
			canc = obj['c_canel']
			outletname = obj['outlet_name']
			invoice = obj['invoice']
			category = obj['category']
			obj['total_bill_value'] = floatconverter(obj['total_bill_value'])
			total_bill_value = round(obj['total_bill_value'], 2)
			food_ready = obj['food_ready']
			payment_mode = obj['payment_mode']
			t = obj['time']
			d = obj['dt']
			if price == 'N/A':
				price = 0
			else:
				price = floatconverter(price)
			if qty == 'N/A':
				qty = 0
			else:
				qty = floatconverter(qty)
			if price > 0 or qty > 0:
				totalprice = price * qty
			else:
				totalprice = 0
			obj['product_discount'] = floatconverter(obj['product_discount'])
			product_discount = obj['product_discount']
			Order_Value_Pre_tax = totalprice - product_discount
			Order_Value_Post_tax = Order_Value_Pre_tax + total_tax
			if varss == '' or varss == 'N/A':
				final_product = str(name)
			else:
				final_product = str(name) + str(' | ') + str(varss)
			sv = 0
			row_num += 1
			row = [
				obj['ab'],
				final_product,
				price,
				qty,
				totalprice,
				category,
				outletname,
				invoice,
				source,
				d,
				t,
				canc,
				food_ready,
				product_discount,
				Order_Value_Pre_tax,
				cgst_percent,
				cgst_value,
				sgst_percent,
				sgst_value,
				cess_percent,
				cess_value,
				total_tax,
				round(Order_Value_Post_tax, 2),
				sv,
				round(Order_Value_Post_tax, 2),
				payment_mode,
				obj["rating"],
				obj["acceptance_time"],
				obj["food_ready_time"],
				obj["kpt_to_dispatch"],
				obj["ttk"]
			]
			for col_num in range(len(row)):
				ws.write(row_num, col_num, row[col_num], font_style)
		import secrets
		a = secrets.token_hex(10)
		file_name = 'Report' + a + '.xls'
		wb.save(file_name)
		from django.core.files import File
		f = open(file_name,'rb')
		myfile = File(f)
		im_name_path = myfile.file.name
		im_size = (os.stat(im_name_path).st_size) / 1024 / 1024
		start_date = dateutil.parser.parse(str(s_date)).date()
		end_date = dateutil.parser.parse(str(e_date)).date()
		report_name = "ProductReport " + str(start_date) + "-" + str(end_date)
		b = Report(auth_id_id=user_id, report_name=report_name, report=myfile, \
				   file_size=im_size, created_at=datetime.now())
		b.save()
		os.remove(file_name)
		return None
	except Exception as e:
		error_create = ReportErrorGenerator.objects.create(error_report=str(e))
		return "error_occured"


class ProductReportCsv(APIView):
	
	"""
	Product  Report  data GET API

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

