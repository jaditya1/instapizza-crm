# import json
#
# from django.db.models import Sum
# from rest_framework import serializers
# from rest_framework.generics import ListAPIView
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
#
# from Dunzo.models import Unprocessed_Order_Quote, Processed_Order_Quote
# from Orders.models import Order
# from Outlet.models import OutletProfile
# from reports.models import Report
# from zapio.settings import Media_Path
#
#
# class UnprocessedQuote(APIView):
#
#     # permission_classes = (IsAuthenticated,)
#     def post(self, request, format=None):
#         try:
#             # data = request.data
#             # user = request.user.id
#             outlet_id = OutletProfile.objects.filter(username='dlfGalleria_gurgaon')
#             if outlet_id.count() != 0:
#                 order_id = Order.objects.filter(outlet=outlet_id[0].id)
#                 if order_id.count() != 0:
#                     order = order_id[0].id
#                 else:
#                     return Response(
#                         {
#                             "success"		: 	False,
#                             "message"			: 	"no order id exits!!"
#                         }
#                     )
#                 headers = {"client-id ":"54515706-95ab-4592-aa5f-4c3f13aad9f8
#                            ","Authorization ":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkIjp7InJvbGUiOjEwMCwidWlkIjoiZGYyMGViZmItZTU2OC00NGM2LWE4MTItNmFlZDlmZWY5MDI4In0sIm1lcmNoYW50X3R5cGUiOm51bGwsImNsaWVudF9pZCI6IjU0NTE1NzA2LTk1YWItNDU5Mi1hYTVmLTRjM2YxM2FhZDlmOCIsImF1ZCI6Imh0dHBzOi8vaWRlbnRpdHl0b29sa2l0Lmdvb2dsZWFwaXMuY29tL2dvb2dsZS5pZGVudGl0eS5pZGVudGl0eXRvb2xraXQudjEuSWRlbnRpdHlUb29sa2l0IiwibmFtZSI6InRlc3RfMjg1MjU2Nzk2OCIsInV1aWQiOiJkZjIwZWJmYi1lNTY4LTQ0YzYtYTgxMi02YWVkOWZlZjkwMjgiLCJyb2xlIjoxMDAsImR1bnpvX2tleSI6ImRmMTQ1YzAwLWIxODItNDk2ZC04MTU3LTA2NWMzOTBmZDRmYyIsImV4cCI6MTc1NjE5MjkwMCwidiI6MCwiaWF0IjoxNjAwNjcyOTAwLCJzZWNyZXRfa2V5IjoiZDc3MTMwNTEtYWRiMi00NTNiLWE3ODktZjY2YzY3NjJkOWQxIn0.MubKcA_EKw0XrWYj9-KyOwBnnADJoizuuXQb93QR0HA"}
#                 url = 'https://apis-staging.dunzo.in/api/v1/quote?pickup_lat=12.9468154&pickup_lng=77.6472151&drop_lat=12.9468354&drop_lng=77.6474151&category_id=pickup_drop'
#
#                 import requests
#                 r = requests.get(ur l,headers=headers)
#                 q = r.json()
#                 un_qoute_data = Unprocessed_Order_Quote(order_quote_id=order_id[0], raw_api_response=q)
#                 un_qoute_data.save()
#                 qoute_data = Processed_Order_Quote(order_quote_id=order_id[0 ],category_id=q['category_id'
#                                                    ],distance=q['distance'],
#                                                    estimated_price=q['estimated_price'],
#                                                    ea= q['eta'])
#                 qoute_data.save()
#
#                 return Response(
#                     {
#                         "success": True,
#                         "dat" : r.json(),
#                         "message"		: 	"success!!"
#                     }
#                 )
#             else:
#                 return Response(
#                     {
#                         "success"		: 	False,
#                         "message"			: 	"no outlet id exits!!"
#                     }
#                 )
#
#         except Exception as e:
#             return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
#
#
