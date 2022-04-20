from Product.models import *
from django.http import HttpResponse



def export_xls(modeladmin, request, queryset):
	import xlwt
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename=ProductReport.xls'
	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet("ProductReport")

	row_num = 0

	columns = [
		("S.No", 2000),
		("Product Id",1000),
		("Product Category", 4000),
		("Product", 6000),
		("Food Type", 2000),
		("Company", 3000),
		("Product Description", 8000),
		("Price", 2000),
		("Discount Price", 2000),
		("Variant Deatils", 8000),
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
		v_details = obj.variant_deatils
		if v_details != None:
			for i in v_details:
				v_q_id = Variant.objects.filter(variant=i["name"])[0].id
				i["v_id"] = v_q_id
		else:
			pass
		row_num += 1
		row = [
			row_num,
			obj.id,
			obj.product_category.category_name,
			obj.product_name,
			obj.food_type.food_type,
			obj.Company.company_name,
			obj.product_desc,
			obj.price,
			obj.discount_price,
			str(v_details)
		]
		for col_num in range(len(row)):
			ws.write(row_num, col_num, row[col_num], font_style)

	wb.save(response)
	return response

export_xls.short_description = "Export Selected to XLS"