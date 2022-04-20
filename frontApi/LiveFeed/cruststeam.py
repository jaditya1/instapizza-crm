from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile, TempTracking, Crustflix_Videos
from rest_framework import serializers

class Crustflixseriaizer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super(Crustflixseriaizer, self).to_representation(instance)
        representation['created_at'] = instance.created_at.strftime("%d/%b/%y %I:%M %p")
        return representation
    class Meta:
        model = Crustflix_Videos
        fields = ['title','youtube_url','active_status','created_at']

class Crustflix(APIView):
    """
    	Active Crust Stream listing GET API

    		Authentication Required		: No
    			Response: {
                        "success": true,
                        "data": [{
                                "id": 1,
                                "youtube_url": "https://www.youtube.com/watch?v=B38aDwUpcFc",
                                "active_status": true,
                                "created_at": "2020-09-12T13:27:50.952138+05:30"
                            },]
                            }


    	"""

    def get(self,request,formet = None):
        qs = Crustflix_Videos.objects.filter(active_status = True).order_by('id')
        serializer_class = Crustflixseriaizer(qs,many=True)
        return Response({
            "success": True,
            "data"	:	serializer_class.data
        })