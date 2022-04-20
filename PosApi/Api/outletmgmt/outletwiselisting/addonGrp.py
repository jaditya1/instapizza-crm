from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Outlet.models import OutletProfile
from Product.models import AddonDetails
from urbanpiper.models import SubCatOutletWiseAddonGroup


class OutletwiseAddonGroup(APIView):
	"""
	Outletwise Addon Group listing POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to retrieve listing of addon groups associated with outlet.

		Data Post: {

			"outlet_id"     : "1"

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
					"success"   :   False,
					"message"   :   "Please select valid outlet!!"
					})
			sub_cat = SubCatOutletWiseAddonGroup.objects.filter(outlet=data['outlet_id'],
													addon_group__active_status=1)
			addongrp_record = AddonDetails.objects.filter(active_status = True,Company=1)
			if sub_cat.count() == 0:
				for q in addongrp_record:
					urban_create = \
					SubCatOutletWiseAddonGroup.objects.create(outlet_id=data['outlet_id'],\
						addon_group_id=q.id)
			else:
				for q in addongrp_record:
					record_check = sub_cat.filter(addon_group_id=q.id)
					if record_check.count()==0:
						urban_create = \
						SubCatOutletWiseAddonGroup.objects.create(outlet_id=data['outlet_id'],\
						addon_group_id=q.id)
					else:
						pass
			final_urban_addongrps = SubCatOutletWiseAddonGroup.objects.filter(outlet=data['outlet_id'],
												addon_group__active_status=1).order_by('addon_group__priority')
			result = []
			for i in final_urban_addongrps:
				data_dict = {}
				data_dict["addon_grp_id"] = i.addon_group_id
				data_dict["addon_grp_name"] = i.addon_group.addon_gr_name
				if i.addon_group.product_variant == None:
					pass
				else:
					data_dict["addon_grp_name"] = \
					data_dict["addon_grp_name"]+" | "+i.addon_group.product_variant.variant
				data_dict["priority"] = i.addon_group.priority
				data_dict["is_available"] = i.is_available
				result.append(data_dict)
			return Response({
				"success"	:	True,
				"data"		:	result
				})
		except Exception as e:
			return Response({
				"success"	: 	False, 
				"message"	: 	"Error happened!!", "errors": str(e)
				})

