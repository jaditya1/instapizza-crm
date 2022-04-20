from django.http import HttpResponse
from Orders.models import Order


def export_product_xls(modeladmin, request, queryset):
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
		("Price", 2000),
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
		row_num += 1
		if obj.variant_id != None:
			product_name = obj.product.product_name+" | "+obj.variant.variant
		else:
			product_name = obj.product.product_name
		row = [
			row_num,
			obj.id,
			obj.product_id,
			product_name,
			obj.price,
			obj.active_status
		]
		for col_num in range(len(row)):
			ws.write(row_num, col_num, row[col_num], font_style)

	wb.save(response)
	return response

export_product_xls.short_description = "Export Selected Product Info to XLS"