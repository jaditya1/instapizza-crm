from Brands.models import Company
from UserRole.models import ManagerProfile
from Outlet.models import OutletProfile

def outlets(user):
	is_brand = Company.objects.filter(auth_user=user)
	result = []
	outlet_ids = []

	if is_brand.count() == 1:
		company_id = is_brand[0].id
		if company_id == 1:
			record = OutletProfile.objects.filter(active_status=1).order_by('Company')
		else:
			record = OutletProfile.objects.filter(active_status=1, Company = company_id)
		for i in record:
			data_dict = {}
			data_dict["id"] = i.id
			data_dict["Outletname"] = i.Outletname
			result.append(data_dict)
			outlet_ids.append(i.id)	
		return {
		"success"		:	True,
		"data"			:	result,
		"outlet_ids"	:	outlet_ids,
		"message"		:	"API worked well!!"
		}
	else:
		pass
	is_outlet = OutletProfile.objects.filter(active_status=1,auth_user=user)
	if is_outlet.count() == 1:
		i = is_outlet[0]
		data_dict = {}
		data_dict["id"] = i.id
		data_dict["Outletname"] = i.Outletname
		result.append(data_dict)
		outlet_ids.append(i.id)	
		return {
			"success"		:	True,
			"data"			:	result,
			"outlet_ids"	:	outlet_ids,
			"message"		:	"API worked well!!"
			}
	else:
		pass
	is_manager = ManagerProfile.objects.filter(auth_user = user, active_status = 1)
	if is_manager.count() == 1:
		ids = is_manager[0].outlet
		for i in ids:
			query = OutletProfile.objects.filter(active_status=1, id=i)
			if query.count() == 0:
				pass
			else:
				q = query[0]
				data_dict = {}
				data_dict["id"] = q.id
				data_dict["Outletname"] = q.Outletname
				result.append(data_dict)
				outlet_ids.append(i)	
	else:
		pass
	return {
			"success"		:	True,
			"data"			:	result,
			"outlet_ids"	:	outlet_ids,
			"message"		:	"API worked well!!"
			}

			
