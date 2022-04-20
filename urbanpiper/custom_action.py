from django.http import HttpResponse
from Orders.models import Order


def export_xls(modeladmin, request, queryset):
	import xlwt
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename=ProductVariantReport.xls'
	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet("ProductReport")

	row_num = 0

	columns = [
		("S.No", 2000),
		("Product Unique Id",3000),
		("Product Id", 2000),
		("Product Name", 8000),
		("Variant Id", 2000),
		("Variant", 4000),
		("Status", 2000)
	]

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num][0], font_style)
		# set column width
		ws.col(col_num).width = columns[col_num][1]

	font_style = xlwt.XFStyle()
	font_style.alignment.wrap = 1

	for obj in queryset:
		if obj.variant_id != None:
			product_name = obj.product.product_name+" | "+obj.variant.variant
			variant_id = obj.variant_id
			variant_name = obj.variant.variant
		else:
			product_name = obj.product.product_name
			variant_name = None
			variant_id = None
		row_num += 1
		row = [
			row_num,
			obj.id,
			obj.product_id,
			product_name,
			variant_id,
			variant_name,
			True
		]
		for col_num in range(len(row)):
			ws.write(row_num, col_num, row[col_num], font_style)

	wb.save(response)
	return response

export_xls.short_description = "Export Selected to XLS"



def sync_order(modeladmin, request, queryset):
	for j in queryset:
		order_id = j.order_id
		urban_order_details = j.order_description
		main_order = Order.objects.filter(urban_order_id=order_id)
		if main_order.count() == 0:
			pass
		else:
			main_order_description = main_order[0].order_description
			for k in main_order_description:
				updated_order_des = []
				for i in urban_order_details:
					order_dict = {}
					order_dict["id"] = i["id"]
					order_dict["name"] = i["title"]
					order_dict["price"] = i["total"]
					order_dict["quantity"] = i["quantity"]
					merchant_id = i["merchant_id"]
					final_product_id = merchant_id.replace('I-','')
					order_dict["final_product_id"] =  final_product_id
					if i["food_type"] == "1":
						order_dict["food_type"] = "Vegetarian"
					else:
						order_dict["food_type"] = "Non Vegetarian"
					order_dict["size"] = ""
					order_dict["customization_details"] = i["options_to_add"]
					for k in i["options_to_add"]:
						addon_merchant_id = k["merchant_id"]
						final_addon_id = addon_merchant_id.replace('A-','')
						k["final_addon_id"] = final_addon_id
					updated_order_des.append(order_dict)
				main_order_update = \
				main_order.update(order_description=updated_order_des)

sync_order.short_description = "Sync Order Manually"