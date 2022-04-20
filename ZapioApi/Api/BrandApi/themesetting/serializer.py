from rest_framework import serializers
from django.db.models import Count
from Configuration.models import ColorSetting



class ThemeSerializer(serializers.ModelSerializer):

	class Meta:
		model = ColorSetting
		fields = '__all__'
