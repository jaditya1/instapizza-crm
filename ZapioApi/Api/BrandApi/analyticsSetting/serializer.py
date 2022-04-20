from rest_framework import serializers
from django.db.models import Count
from Configuration.models import AnalyticsSetting



class AnalyticsSerializer(serializers.ModelSerializer):

	class Meta:
		model = AnalyticsSetting
		fields = '__all__'