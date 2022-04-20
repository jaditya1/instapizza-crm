from django.db.models import Sum
from rest_framework import serializers
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Brands.models import Company
from Configuration.models import ColorSetting, TaxSetting, PaymentDetails
from Outlet.models import OutletProfile, OutletMilesRules
from reports.models import Report
from zapio.settings import Media_Path
from rest_framework import parsers

class Dropboxdeleting(APIView):
    """
	   Report Delete data POST API

			Authentication Required		: Yes
			Service Usage & Description	: Download Product csv file

			Data Post:
    			{
    				"id" : 12
    			}


		    Response: {

				"success": true,
                "message": "Report delete successful!!"
    			}

    		"""

    permission_classes = (IsAuthenticated,)
    def delete(self, request, format=None):

        try:
            data = request.data
            user = request.user.id
            query = Report.objects.get(id=data['id'])
            query.delete()
            return Response({
                        "success"			: 	True,
                        "message"			: 	"Report delete successful!!"
                    })
        except Exception as e:
            return Response({"success": False, "message": "Error happened!!", "errors": str(e)})

class Dropboxlisting(APIView):
    """
     		 get Report list Delete data GET API

     			Authentication Required		: Yes
     			Service Usage & Description	: .Download Product csv file


     			Response: {

     				 {
    "success": true,
    "data": [
        {
            "id": 41,
            "report_name": "outlet_log 2020-08-15-2020-08-17",
            "report": "https://admin.instapos.in/media/xls_reports/Report6672e9359f58a3d9f7a2.xls",
            "created_at": "08/Sep/20",
            "file_size": 0.00537109375
                },
            ],
            "remaining_space": 99.05,
            "used_space"     : 0.95
            "message": "Addon details fetching successful!!"
        }
                        }

     		"""
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        try:
            data = request.data
            user = request.user.id
            query = Report.objects.\
                        filter(auth_id=user).order_by('-created_at')

            result = []
            for q in query:
                q_dict = {}
                q_dict["id"] = q.id
                q_dict["report_name"] = q.report_name
                q_dict["report"] = Media_Path+str(q.report)
                # q_dict["report"] = q.report
                q_dict['created_at'] = q.created_at.strftime("%d/%b/%y")
                q_dict['file_size'] = q.file_size
                result.append(q_dict)

            used_space = query.aggregate(Sum('file_size'))['file_size__sum'] or 0
            remaining_space = round((100-used_space),2)
            return Response(
                    {
                        "success"			: 	True,
                        "data" 				: 	result,
                        "remaining_space"	:	remaining_space,
                        "used_space"        :   used_space,
                        "message"			: 	"Reports details fetched successful!!"
                    }
                    )
        except Exception as e:
            return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


