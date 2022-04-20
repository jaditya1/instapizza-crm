from rest_framework.views import APIView
from rest_framework.response import Response
from UserRole.models import UserType, MainRoutingModule, RoutingModule, SubRoutingModule
from rest_framework.permissions import IsAuthenticated

class ModuleListing(APIView):
	"""
	Module listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of module data within brand.
	"""
	# permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			record = MainRoutingModule.objects.filter(active_status=1)
			final_result = []
			if record.count() > 0:
				for i in record:
					record_dict = {}
					record_dict['module_id'] = i.module_id
					record_dict['icon'] = i.icon
					record_dict['label'] = i.label
					record_dict['to'] = i.to
					record_dict['component'] = i.component
					route_record = RoutingModule.objects.filter(active_status=1,main_route=i.id)
					if route_record.count() != 0:
						record_dict['subs'] = []
						for j in route_record:
							route_dict = {}
							route_dict['icon'] = j.icon
							route_dict['label'] = j.label
							route_dict['to'] = j.to
							route_dict['component'] = j.component
							# record_dict['subs'].append(route_dict)
							sub_route_record = \
							SubRoutingModule.objects.filter(active_status=1,route=j.id)
							if sub_route_record.count() != 0:
								route_dict['subs'] = []
								for k in sub_route_record:
									sub_route_dict = {}
									sub_route_dict['icon'] = k.icon
									sub_route_dict['label'] = k.label
									sub_route_dict['to'] = k.to
									sub_route_dict['component'] = k.component
									route_dict['subs'].append(sub_route_dict)
							else:
								pass
							record_dict['subs'].append(route_dict)
					else:
						pass
					final_result.append(record_dict)
				return Response({
						"success": True, 
						"data": final_result})
			else:
				return Response({
						"success": True, 
						"data": []})
		except Exception as e:
			print("Module listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})