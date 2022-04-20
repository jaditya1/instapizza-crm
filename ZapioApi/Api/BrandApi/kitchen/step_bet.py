from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime

#Serializer for api
from rest_framework import serializers
from Product.models import ProductCategory
from kitchen.models import StepToprocess, ProcessTrack
from Product.models import Product,Variant
from django.db.models import Max,Min
from ZapioApi.Api.BrandApi.kitchen.process_bet_error_check import *
from Brands.models import Company
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user



class StepProcessBetween(APIView):

	"""
	Step process Between POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to between step process and sync remaining ones accordingly.

		Data Post: {
			"after_step"		           : "1",
			"product"		               : "3",
			"varient"                      : "1",
			"process"                      : "www",
			"description"                  : "sadsadsa",
			"time_of_process"              : "20",
			"image"                        : "pizza.jpg",
 			"ingrediate"                   : [
				{
					"name"           : "Large",
					"unit"           : "gms",
					"id"             : "1",
					"quantitiy"      : "4"
			    }],
		}

		Response: {

			"success": True, 
			"message": "Step deleted successfully!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			data["company_auth_id"] = request.user.id
			data2 = json.loads(data["ingrediate"])
			data['ingrediate'] = data2
			validation_check = err_check(data)
			if validation_check != None:
				return Response(validation_check) 
			pro_query = Product.objects.filter(id=data["product"])
			Company_id = Company.objects.filter(auth_user=data["company_auth_id"])[0].id
			if pro_query.count() != 0:
				pass
			else:
				return Response(
					{
						"success": False,
						"message": "Product is not valid!!"
					}
					)
			if data["varient"] != "":
				sucat_query = Variant.objects.filter(id=data["varient"])
				if sucat_query.count() != 0:
					pass
				else:
					return Response(
						{
							"success": False,
							"message": "Varient id is not valid to update!!"
						}
						)
			else:
				pass
			p_id = data['product']
			v_id = data['varient']
			process_data = StepToprocess.objects.filter(product_id=p_id,varient_id=v_id)
			if process_data.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Required Process data is not valid to retrieve!!"
				}
				)	
			else:
				p_id = process_data[0].product_id
				v_id = process_data[0].varient_id
				process_data = StepToprocess.objects.filter(product_id=p_id,varient_id=v_id)
				stp = []
				for i in process_data:
					stp.append(i.step)
				mstep = max(stp) + 1
				chs = int(data['after_step']) + 1
				if int(data['after_step']) in stp or int(data['after_step'])==0 or mstep == chs:
					data["active_status"] = 1
					if mstep == int(data['after_step']):
						p_query = \
						StepToprocess.objects.create(company_id=Company_id,\
						product_id=data["product"],varient_id=data["varient"],\
						step=data['after_step'],process=data["process"],description=data["description"],\
						time_of_process=int(data["time_of_process"]),image=data["image"],\
						ingredient=data["ingrediate"],\
						active_status=data["active_status"],created_at=datetime.now(),\
						 )
					else:
						df = int(data['after_step'])
						pro_data = StepToprocess.objects.filter(step__gt=df, product_id=p_id,varient_id=v_id).order_by('step')
						for i in pro_data:
							ids = i.id
							st = i.step+1
							p_data = StepToprocess.objects.filter(id=ids)
							p_data.update(step=st)
						new_step = int(data['after_step']) + 1
						p_query = \
							StepToprocess.objects.create(company_id=Company_id,\
							product_id=data["product"],varient_id=data["varient"],\
							step=new_step,process=data["process"],description=data["description"],\
							time_of_process=int(data["time_of_process"]),image=data["image"],\
							ingredient=data["ingrediate"],\
							active_status=data["active_status"],created_at=datetime.now(),\
						)
				else:
					err_message = {}
					err_message["after_step"] = "Product process step not allowed!!"
					return Response({
						"success": False, 
						"error" : err_message
						})

				return Response({
						"success": True, 
						"message": "Product process is created successfully!!"
						})
		except Exception as e:
				print("Step process Delete Api Stucked into exception!!")
				print(e)
				return Response({"success": False, 
								"message": "Error happened!!", 
								"errors": str(e)})
