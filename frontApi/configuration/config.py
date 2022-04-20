from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import re
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from Brands.models import Company
from _thread import start_new_thread
from datetime import datetime
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
import json
from zapio.settings import Media_Path
from  Configuration.models import ColorSetting


class ConfigView(APIView):
	"""
	Configuration data listing GET API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for providing config data of brand.

	"""
	def get(self, request, format=None):
		try:
			postdata = request.META
			url = postdata['HTTP_ORIGIN']
			# url = "https://instapizza.in"
			if url:
				data = Company.objects.filter(website=url)
				if data.count()!=0:
					company_data = data[0]
					c_id = company_data.id
					p_list={}
					pdata = []
					color_q = \
					ColorSetting.objects.filter(company=c_id,active_status=1)
					if color_q.count()!=0:
						p_list["accent_color"] = color_q[0].accent_color 
						p_list["textColor"] = color_q[0].textColor
						p_list["secondaryColor"] = color_q[0].secondaryColor
						p_list["brand_name"] = color_q[0].company.company_name
					else:
						return Response({"success": False,
							     "message":"Color Parameter is not set at super-admin level!!"})
					if company_data.company_logo != "" and company_data.company_logo != None:
						full_path = Media_Path + str(company_data.company_logo)
						p_list['logo'] = full_path
					if company_data.company_landing_imge != "" and company_data.company_landing_imge != None:
						full_path1 = Media_Path + str(company_data.company_landing_imge)
						p_list['banner'] = full_path1
					p_list['company'] = company_data.id
					pdata.append(p_list)
					return Response({"success":True,
								     "data":pdata})
				else:
					return Response({"success":True,
								     "data":[]})
			else:
				return Response({"success": False,
							     "message":"Url not Found!!"})
		except Exception as e:
			print(e)
			return Response({"success": False,
							"message":"config api stucked into exception!!"})
