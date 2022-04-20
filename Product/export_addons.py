from Product.models import *
from django.http import HttpResponse



def export_xls(modeladmin, request, queryset):
	import xlwt
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename=AddonReport.xls'
	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet("AddonReport")

	row_num = 0

	columns = [
		("S.No", 2000),
		("Addon Id",1000),
		("Addon Group", 4000),
		("Addon", 6000),
		("Company", 3000),
		("Price", 2000),
		("Active Status", 8000),
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
		addon_grp = obj.addon_group_id 
		if obj.addon_group_id == None:
			addon_grp = None
		else:
			addon_grp = obj.addon_group.addon_gr_name
		row_num += 1
		row = [
			row_num,
			obj.id,
			addon_grp,
			obj.name,
			obj.Company.company_name,
			obj.addon_amount,	
			obj.active_status	
			]
		for col_num in range(len(row)):
			ws.write(row_num, col_num, row[col_num], font_style)

	wb.save(response)
	return response

export_xls.short_description = "Export Selected to XLS"