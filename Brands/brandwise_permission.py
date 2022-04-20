from django.db.models import Q
from UserRole.models import UserType, MainRoutingModule, RollPermission, BillingMainRoutingModule, \
BillRollPermission


def Rollpermit(brand_id, user_type_id):
	allmenu = MainRoutingModule.objects.filter(active_status=1)
	for i in allmenu:
		main_route = i.id
		company = brand_id
		user_type = user_type_id
		roll_record = RollPermission.objects.filter(Q(company=company),Q(user_type_id=user_type),\
										Q(main_route_id=main_route))
		if roll_record.count() == 0:
			roll_create = \
			RollPermission.objects.create(user_type_id=user_type,main_route_id=main_route,\
							company_id=company,label=1)
		else:
			roll_update = \
			roll_record.update(user_type_id=user_type,main_route_id=main_route,company_id=company,\
								label=1)



def BillRollpermit(brand_id, user_type_id):
	allmenu = BillingMainRoutingModule.objects.filter(active_status=1)
	for i in allmenu:
		main_route = i.id
		company = brand_id
		user_type = user_type_id
		roll_record = BillRollPermission.objects.filter(Q(company=company),Q(user_type_id=user_type),\
										Q(main_route_id=main_route))
		if roll_record.count() == 0:
			roll_create = \
			BillRollPermission.objects.create(user_type_id=user_type,main_route_id=main_route,\
								label=1,company_id=company)
		else:
			roll_update = \
			roll_record.update(user_type_id=user_type,main_route_id=main_route,company_id=company,\
								label=1)



def SaveRoll(Company_id):
	try:
		data = {}
		userdata = UserType.objects.filter(active_status=1).order_by('id')
		for i in userdata:
			user_type = i.id
			Rollpermit(Company_id, user_type)
			BillRollpermit(Company_id, user_type)
		return None
	except Exception as e:
		print(e)
		return str(e)
