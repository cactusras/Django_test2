from rest_framework import serializers
from .models import WorkingHour

class WorkingHourSerializer(serializers.ModelSerializer):
    start_time = serializers.TimeField(format='%H:%M', input_formats=['%H:%M'])
    end_time = serializers.TimeField(format='%H:%M', input_formats=['%H:%M'])

    class Meta:
        model = WorkingHour
        fields = ['day_of_week', 'start_time', 'end_time']