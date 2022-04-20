from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Outlet.models import OutletProfile
from urbanpiper.models import SubCatOutletWiseAddonGroup, SubCatOutletWiseAddons, ProductSync
from datetime import datetime
from Product.models import AddonDetails, Addons


class OutletwiseAddons(APIView):

	"""
	Associated Addons Outletwise POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to retrieve listing of addons associated with outlet based on Addon Group and outlet.

		Data Post: {

			"outlet_id"     	: 	"1",
			"addon_grp_id"		:	"20"

		}

		Response: {

			"success"	:	True,
			"data"		:	result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			outlet_id = OutletProfile.objects.filter(id=data['outlet_id'], active_status=1)
			if outlet_id.count() != 0:
				pass
			else:
				return Response({
					"success"	: 	False,
					"message"	: 	"Please select valid outlet!!"
					})
			addon_grp = AddonDetails.objects.filter(id=data["addon_grp_id"],active_status=1)
			if addon_grp.count() != 0:
				pass
			else:
				return Response({
					"success"	: 	False,
					"message"	: 	"Please select valid Addon Group!!"
					})
			sub_cat = SubCatOutletWiseAddons.objects.filter(outlet = data['outlet_id'], 
										addon_id__addon_group=data["addon_grp_id"],addon_id__active_status=1)
			addon_record = Addons.objects.filter(addon_group=data["addon_grp_id"],active_status=1, \
																			addon_group__active_status=1)
			if sub_cat.count() == 0:
				for q in addon_record:
					urban_create = \
					SubCatOutletWiseAddons.objects.create(outlet_id=data['outlet_id'],addon_id_id=q.id)
			else:
				for q in addon_record:
					record_check = sub_cat.filter(addon_id=q.id)
					if record_check.count()==0:
						urban_create = \
						SubCatOutletWiseAddons.objects.create(outlet_id=data['outlet_id'],addon_id_id=q.id)
					else:
						pass
			final_urban_addons = SubCatOutletWiseAddons.objects.filter(outlet = data['outlet_id'], 
							addon_id__addon_group=data["addon_grp_id"],addon_id__active_status=1,\
							addon_id__addon_group__active_status=1).order_by('addon_id__priority')
			result = []
			for i in final_urban_addons:
				data_dict = {}
				data_dict["addon_id"] = i.addon_id_id
				data_dict["addon_name"] = i.addon_id.name
				data_dict["price"] = i.addon_id.addon_amount
				data_dict["is_available"] = i.is_available
				data_dict["priority"] = i.addon_id.priority
				result.append(data_dict)
			return Response({
				"success"	:	True,
				"data"		:	result
				})
		except Exception as e:
			return Response({
				"success"	: 	False, 
				"message"	: 	"Error happened!!", 
				"errors"	: 	str(e)
				})