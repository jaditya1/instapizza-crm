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
from Configuration.models import *
from discount.models import PercentOffers
from Outlet.models import DeliveryBoy,OutletProfile
from UserRole.models import ManagerProfile
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from zapio.settings import Media_Path


class DeliveryList(APIView):
	"""
	Delivery Boy Listing POST API
		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Delivery Boy data within brand.
	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		user = self.request.user.id
		auth_id = request.user.id
		user = request.user.id
		cid = get_user(user)
		delivery_data = DeliveryBoy.objects.filter(Company=cid).order_by('id')
		if delivery_data.count() > 0:
			pro_data =[]
			for i in delivery_data:
				p_list ={}
				p_list['id'] = i.id
				p_list['name'] = i.name
				p_list['email'] = i.email
				p_list['mobile'] = i.mobile
				p_list['address'] = i.address
				p_list['profile_pic'] = str(i.profile_pic)
				p_list['active_status'] = i.active_status
				domain_name = Media_Path
				if i.profile_pic != "" and i.profile_pic != None:
					full_path = domain_name + str(i.profile_pic)
					p_list['profile_pic'] = full_path
				pro_data.append(p_list)
			return Response({"status":True,
							"data":pro_data})
		else:
			return Response({"status":True,
							"data":[]})



