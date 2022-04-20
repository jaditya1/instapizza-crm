import os
import sys
from datetime import datetime
from _thread import start_new_thread
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
from Outlet.models import *
from UserRole.models import ManagerProfile
from datetime import datetime, timedelta
from reports.models import Report, ReportErrorGenerator
from django.db.models import Sum


def reportscsv(s_date,e_date,outletss,user_id):
	try:
		import xlwt
		wb = xlwt.Workbook()
		ws = wb.add_sheet("order_report")
		row_num = 0
		columns = [
			("Order & Invoice Details", 10000),
			("Order Value Details", 10000),
			("Order Mertics Details", 10000),
		]
		font_style = xlwt.XFStyle()
		font_style.font.bold = True

		pattern = xlwt.Pattern()
		pattern.pattern = xlwt.Pattern.SOLID_PATTERN
		pattern.pattern_fore_colour = xlwt.Style.colour_map['blue']  # Set the cell background color to yellow
		font_style.pattern = pattern

		ws.write_merge(0, 0, 0, 13, 'Order & Invoice Details', xlwt.easyxf(
			'align:horiz centre; pattern: pattern solid, fore_color gray25;  font: color black,bold on,height 200'))
		ws.write_merge(0, 0, 14, 25, 'Order Value Details', xlwt.easyxf(
			'align:horiz centre; pattern: pattern solid, fore_color orange;  font: color white,bold on,height 200'))
		ws.write_merge(0, 0, 26, 32, 'Order Status Details', xlwt.easyxf(
			'align:horiz centre; pattern: pattern solid, fore_color blue;  font: color white,bold on,height 200'))
		ws.write_merge(0, 0, 33, 35, 'Rider Details', xlwt.easyxf(
			'align:horiz centre; pattern: pattern solid, fore_color orange;  font: color white,bold on,height 200'))
		ws.write_merge(0, 0, 36, 53, 'Payment Modes', xlwt.easyxf(
			'align:horiz centre; pattern: pattern solid, fore_color blue;  font: color white,bold on,height 200'))
		ws.write_merge(0, 0, 54, 65, 'Order Metrics', xlwt.easyxf(
			'align:horiz centre; pattern: pattern solid, fore_color green;  font: color white,bold on,height 200'))
		# ws.col(col_num).width = columns[col_num][16]

		font_style = xlwt.XFStyle()
		font_style.alignment.wrap = 1

		date_format = xlwt.XFStyle()
		date_format.num_format_str = 'dd/mm/yyyy'

		row_num = 1
		columns = [
			("Outlet ID", 3000),
			("Outlet Name", 3000),
			("User", 3000),
			("IP_Invoice", 3000),
			("Order_Date", 3000),
			("Order_Time", 3000, date_format),
			("Order Type", 3000),
			("Delivery Type", 3000),
			("Customer_Name", 3000),
			("Customer_Contact", 3000),
			("Order_Source", 3000),
			("Aggregator_Rest#", 3000),
			("Total", 3000),
			("URBAN ORDER ID", 3000),
			("CHANNEL ORDER ID", 3000),
			("Order_GMV", 3000),
			("Order_Value_Subtotal", 3000),
			("Total_Discount", 3000),
			("External Discount", 3000),
			("Discount Name", 3000),
			("Discount Reason", 3000),
			("Packaging_Charges", 3000),
			("Service_Charges", 3000),
			("Order_Value_Pre_tax#", 3000),
			("Tax_CGST", 3000),
			("Tax_SGST", 3000),
			("Tax_CESS", 3000),
			("Tax_Total", 3000),
			("Order_Value_Post-Tax", 3000),
			("Short & Excess_Round Off", 3000),
			("Total_Bill_Value", 3000),
			("Order_Status", 3000),
			("Cancellation_Responsible", 3000),
			("Cancellation_Reson", 3000),
			("Received Time", 3000),
			("Accepted in Time", 3000),
			("Food Ready in Time", 3000),
			("Dispatched in Time", 3000),
			("Rider Name", 3000),
			("Mobile", 3000),
			("COD", 3000),
			("Dineout", 3000),
			("Paytm", 3000),
			("Razorpay", 3000),
			("PayU", 3000),
			("EDC", 3000),
			("Mobiquik", 3000),
			("EDC Amex", 3000),
			("EDC Yes Bank", 3000),
			("SWIGGY", 3000),
			("Z Prepaid", 3000),
			("S Prepaid", 3000),
			("Dunzo", 3000),
			("Zomato", 3000),
			("Zomato Cash", 3000),
			("Magic Pin", 3000),
			("Easy Dinner", 3000),
			("Transition Id", 3000),
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
		cdata = Order.objects.filter(Q(order_time__lte=e_date), Q(order_time__gte=s_date))
		for i in outletss:
			data = cdata.filter(outlet_id=i).order_by('-order_time')
			for obj in data:
				track_order = OrderTracking.objects.filter(Q(order_id=obj.id), \
														   Q(Order_staus_name_id=1))
				if track_order.count() > 0:
					o = track_order[0].created_at
					q = o + timedelta(hours=5, minutes=30)
					s = q.time()
					a = str(s).split('.')
					frd = a[0]
				else:
					frd = 'N/A'
				atimes = OrderTracking.objects.filter(Q(order_id=obj.id), \
													  Q(Order_staus_name_id=2))
				if atimes.count() > 0:
					o = atimes[0].created_at
					q = o + timedelta(hours=5, minutes=30)
					s = q.time()
					a = str(s).split('.')
					act = a[0]
				else:
					act = 'N/A'
				fready = OrderTracking.objects.filter(Q(order_id=obj.id), \
													  Q(Order_staus_name_id=3))
				if fready.count() > 0:
					o = fready[0].created_at
					q = o + timedelta(hours=5, minutes=30)
					s = q.time()
					a = str(s).split('.')
					fredy = a[0]
				else:
					fredy = 'N/A'
				disp = OrderTracking.objects.filter(Q(order_id=obj.id), \
													Q(Order_staus_name_id=4))
				if disp.count() > 0:
					o = disp[0].created_at
					q = o + timedelta(hours=5, minutes=30)
					s = q.time()
					a = str(s).split('.')
					dredy = a[0]
				else:
					dredy = 'N/A'
				if track_order.count() > 0 and atimes.count() > 0:
					date_format = "%H:%M:%S"
					t1 = datetime.strptime(str(frd), date_format)
					t2 = datetime.strptime(str(act), date_format)
					dif = t2 - t1
					sec = dif.total_seconds()
					# diff = sec // 60
					diff = dif
				else:
					diff = 'N/A'
				if fready.count() > 0 and atimes.count() > 0:
					date_format = "%H:%M:%S"
					t1 = datetime.strptime(str(act), date_format)
					t2 = datetime.strptime(str(fredy), date_format)
					f = t2 - t1
					sec = f.total_seconds()
					# fdiff = sec // 60
					fdiff = f
				else:
					fdiff = 'N/A'
				if fready.count() > 0 and disp.count() > 0:
					date_format = "%H:%M:%S"
					t1 = datetime.strptime(str(fredy), date_format)
					t2 = datetime.strptime(str(dredy), date_format)
					f = t2 - t1
					sec = f.total_seconds()
					ddiff = f
				# ddiff = sec // 60
				else:
					ddiff = 'N/A'

				outlet_id = obj.outlet_id
				if outlet_id != None:
					outlet_name = OutletProfile.objects.filter(id=outlet_id)[0].Outletname
				else:
					outlet_name = 'N/A'
				if obj.is_rider_assign == True:
					if obj.is_aggregator == False:
						ad = DeliveryBoy.objects.filter(id=obj.delivery_boy_id)
						rname = ad[0].name
						rmobile = ad[0].mobile
						remail = 'N/A'
					else:
						r = obj.delivery_boy_details
						if r != None:
							rname = r['name']
							rmobile = r['mobile']
							remail = r['email']
						else:
							rname = 'N/A'
							rmobile = 'N/A'
							remail = 'N/A'
				else:
					rname = 'N/A'
					rmobile = 'N/A'
					remail = 'N/A'
				if obj.customer != None:
					user = obj.customer
					if 'name' in user:
						users = user['name']
					else:
						users = 'N/A'

					if 'mobile' in user:
						mobile = user['mobile']
					else:
						mobile = 'N/A'
				else:
					users = 'N/A'

				if obj.taxes:
					tax = round(obj.taxes / 2, 2)
				else:
					tax = 0
				modes = []
				if obj.tax_detail != None:
					if 'CGST' in obj.tax_detail:
						cgst = obj.tax_detail['CGST']
					else:
						cgst = 0
					if 'SGST' in obj.tax_detail:
						sgst = obj.tax_detail['SGST']
					else:
						sgst = 0
					if 'CESS' in obj.tax_detail:
						cess = obj.tax_detail['CESS']
					else:
						cess = 0
				else:
					cgst = round(obj.taxes / 2, 2)
					sgst = round(obj.taxes / 2, 2)
					cess = 0

				cod = 0
				Dineout = 0
				Paytm = 0
				Razorpay = 0
				PayU = 0
				EDC = 0
				Mobiquik = 0
				mix = 0
				Amex = 0
				yes = 0
				swiggy = 0
				z_prepaid = 0
				s_prepaid = 0
				dunzo = 0
				zcash = 0
				zomato = 0
				magic_pin = 0
				easy_dinner = 0
				if obj.settlement_details != None:
					if len(obj.settlement_details) > 0:
						for i in obj.settlement_details:
							if i['mode'] == 0:
								c = float(i['amount'])
								cod = round(c, 2)
							else:
								pass
							if i['mode'] == 1:
								D = float(i['amount'])
								Dineout = round(D, 2)
							else:
								pass
							if i['mode'] == 2:
								P = float(i['amount'])
								Paytm = round(P, 2)
							else:
								pass
							if i['mode'] == 3:
								R = float(i['amount'])
								Razorpay = round(R, 2)
							else:
								pass
							if i['mode'] == 4:
								P = float(i['amount'])
								PayU = round(P, 2)
							else:
								pass
							if i['mode'] == 5:
								e = float(i['amount'])
								EDC = round(e, 2)
							else:
								pass
							if i['mode'] == 6:
								m = float(i['amount'])
								Mobiquik = round(m, 2)
							else:
								pass
							if i['mode'] == 7:
								m = float(i['amount'])
								mix = round(m, 2)
							else:
								pass
							if i['mode'] == 8:
								A = float(i['amount'])
								Amex = round(A, 2)
							else:
								pass
							if i['mode'] == 9:
								y = float(i['amount'])
								yes = round(y, 2)
							else:
								pass
							if i['mode'] == 10:
								s = float(i['amount'])
								swiggy = round(s, 2)
							else:
								pass
							if i['mode'] == 11:
								z = float(i['amount'])
								z_prepaid = round(z, 2)
							else:
								pass
							if i['mode'] == 12:
								sp = float(i['amount'])
								s_prepaid = round(sp, 2)
							else:
								pass
							if i['mode'] == 13:
								do = float(i['amount'])
								dunzo = round(do, 2)
							else:
								pass
							if i['mode'] == 14:
								z = float(i['amount'])
								zcash = round(z, 2)
							else:
								pass
							if i['mode'] == 15:
								zp = float(i['amount'])
								zomato = round(zp, 2)
							else:
								pass
							if i['mode'] == 16:
								mp = float(i['amount'])
								magic_pin = round(mp, 2)
							else:
								pass
							if i['mode'] == 17:
								e_d = float(i['amount'])
								easy_dinner = round(e_d, 2)
							else:
								pass
				else:
					pass

				if zomato == 0 and zcash == 0 and dunzo == 0 and s_prepaid == 0 and \
						z_prepaid == 0 and swiggy == 0 and yes == 0 and Amex == 0 and \
						mix == 0 and Mobiquik == 0 and EDC == 0 and PayU == 0 and \
						Razorpay == 0 and Paytm == 0 and Dineout == 0 and cod == 0 and \
						easy_dinner == 0 and magic_pin == 0:
					if obj.payment_mode == None:
						pass
					else:
						pay = int(obj.payment_mode)
						total_payable_value = obj.total_bill_value
						if pay == 0:
							cod = total_payable_value
						elif pay == 1:
							Dineout = total_payable_value
						elif pay == 2:
							Paytm = total_payable_value
						elif pay == 3:
							Razorpay = total_payable_value
						elif pay == 4:
							PayU = total_payable_value
						elif pay == 5:
							EDC = total_payable_value
						elif pay == 6:
							Mobiquik = total_payable_value
						elif pay == 7:
							mix = total_payable_value
						elif pay == 8:
							Amex = total_payable_value
						elif pay == 9:
							yes = total_payable_value
						elif pay == 10:
							swiggy = total_payable_value
						elif pay == 11:
							z_prepaid = total_payable_value
						elif pay == 12:
							s_prepaid = total_payable_value
						elif pay == 13:
							dunzo = total_payable_value
						elif pay == 14:
							zcash = total_payable_value
						elif pay == 15:
							zomato = total_payable_value
						elif pay == 16:
							magic_pin = total_payable_value
						elif pay == 17:
							easy_dinner = total_payable_value
						else:
							pass
				else:
					pass

				if obj.external_discount != None:
					external_discount = obj.external_discount
				else:
					external_discount = 0
				total_value = \
					(zomato + zcash + dunzo + s_prepaid + z_prepaid + swiggy + yes + Amex + mix + Mobiquik + \
					 EDC + PayU + Razorpay + Paytm + Dineout + cod + easy_dinner + magic_pin) + external_discount
				o_time = obj.order_time + timedelta(hours=5, minutes=30)
				date_format = xlwt.XFStyle()
				date_format.num_format_str = 'dd/MM/yyyy'
				order_time = (o_time.strftime("%I:%M %p"))
				order_date = (o_time.strftime("%d/%b/%y"))
				if obj.sub_total != None:
					tv = obj.sub_total
				else:
					tv = 0
				if obj.discount_value != None:
					dv = obj.discount_value
				else:
					dv = 0
				if obj.packing_charge != None:
					pc = obj.packing_charge
				else:
					pc = 0
				if obj.delivery_charge != None:
					dc = obj.delivery_charge
				else:
					dc = 0
				ip_discount = dv - external_discount
				# Order_Value_Pre_tax = round(float(tv) - float(dv)+\
				#   float(pc) + float(dc),2)

				Order_Value_Pre_tax = round(float(tv) - float(ip_discount) + \
											float(pc) + float(dc), 2)
				if cod == '':
					cod = 0
				else:
					cod = cod
				if swiggy == '':
					swiggy = 0
				else:
					swiggy = swiggy
				codswiggy = cod + swiggy
				if obj.taxes != None:
					t = obj.taxes
				else:
					t = 0

				if obj.sub_total != None:
					ts = obj.sub_total
				else:
					ts = 0
				order_GMV = round(float(ts) + float(t), 2)
				or_post_tax = round(Order_Value_Pre_tax + float(t), 2)
				dreason = ''
				row_num += 1
				if obj.urban_order_id != None:
					urban_order_id = int(obj.urban_order_id)
				else:
					urban_order_id = None
				if obj.channel_order_id != None:
					channel_order_id = int(obj.channel_order_id)
				else:
					channel_order_id = None
				if obj.order_source == "Website":
					custmer_detail = obj.customer
					if "mobile_number" in custmer_detail:
						mobile = str(custmer_detail["mobile_number"])
					else:
						mobile = "N/A"
				else:
					pass
				if obj.rating != None and obj.rating != "":
					rating = obj.rating
				else:
					rating = "N/A"
				process_log_record = \
					OrderProcessTimeLog.objects.filter(order=obj.id)
				if process_log_record.count() == 1:
					process_q = process_log_record[0]
					acceptance_time = process_q.order_acceptance_time
					food_ready_time = process_q.kpt
					kpt_to_dispatch = process_q.kpt_to_dispatch
					ttk = (acceptance_time + food_ready_time + kpt_to_dispatch)
				else:
					acceptance_time = "N/A"
					food_ready_time = "N/A"
					kpt_to_dispatch = "N/A"
					ttk = "N/A"
				zomato = zomato + external_discount
				row = [
					int(outlet_id),
					outlet_name,
					obj.user,
					obj.outlet_order_id,
					o_time.date(),
					o_time.time(),
					obj.order_type,
					obj.delivery_type,
					users,
					mobile,
					obj.order_source,
					'N/A',
					total_value,
					urban_order_id,
					channel_order_id,
					order_GMV,
					obj.sub_total,
					ip_discount,
					obj.external_discount,
					obj.discount_name,
					obj.discount_reason,
					str(pc),
					str(dc),
					Order_Value_Pre_tax,
					cgst,
					sgst,
					cess,
					obj.taxes,
					or_post_tax,
					'N/A',
					or_post_tax,
					# obj.total_bill_value,
					str(obj.order_status),
					obj.cancel_responsibility,
					obj.order_cancel_reason,
					frd,
					str(diff),
					str(fdiff),
					str(ddiff),
					rname,
					rmobile,
					cod,
					Dineout,
					Paytm,
					Razorpay,
					PayU,
					EDC,
					Mobiquik,
					Amex,
					yes,
					swiggy,
					z_prepaid,
					s_prepaid,
					dunzo,
					zomato,
					zcash,
					magic_pin,
					easy_dinner,
					obj.transaction_id,
					rating,
					acceptance_time,
					food_ready_time,
					kpt_to_dispatch,
					ttk
				]
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
		report_name = "OrderReport "+str(start_date)+"-"+str(end_date)
		b = Report(auth_id_id = user_id,report_name=report_name,report=myfile,\
								file_size = im_size,created_at = datetime.now())
		b.save()
		os.remove(file_name)
		return None
	except Exception as e:
		error_create = ReportErrorGenerator.objects.create(error_report=str(e))
		return "error_occured"



def Reportsvaidation(s_date,e_date,data,err_message,user_id):
	try:
		start_date = dateutil.parser.parse(s_date)
		end_date = dateutil.parser.parse(e_date)
		if start_date < end_date:
			pass
		else:
			err_message["date"] = "Please provide meaning full date range!!"
	except Exception as e:
		err_message["date"] = "Please provide meaning full date range!!"
	if len(data["outlet_ids"]) == 0:
		err_message["outlet"] = "Please select at least one id!!"
	else:
		for i in data["outlet_ids"]:
			try:
				i = int(i)
			except Exception as e:
				err_message["outlet"] = "Id is not valid!!"
				break
	if any(err_message.values()) == True:
		return Response({
			"success": False,
			"error" : 	err_message,
			"message" 	: 	"Please correct listed errors!!"
		})
	outletss = data["outlet_ids"]
	# user_id = request.user.id
	report_record = Report.objects.filter(auth_id=user_id)
	total_reports =  \
	report_record.aggregate(Sum('file_size'))['file_size__sum'] or 0
	if total_reports<100:
		pass
	else:
		err_message["dropbox"] = "Please delete some reports from your dropbox to"+\
								" generate new one!!"
		return Response({
			"success"	: 	False,
			"error" 	: 	err_message,
			"message" 	: 	"Please correct listed errors!!"
		})
	return None


def correct_response():
	return Response({
				"success"	 :	True,
				"message"	 : 'Request has been queued...check dropbox after some time!!'
				})


class Ordercsv(APIView):

	"""
	Order data POST API

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
			s_date = data['start_date']
			e_date = data['end_date']
			user_id = request.user.id
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
