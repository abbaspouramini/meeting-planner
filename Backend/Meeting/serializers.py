from rest_framework import serializers
from .models import Meeting , OwnerAvailableTimes

class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ['title','duration','phone_number','address','language','message','url']


class MeetingTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model=OwnerAvailableTimes
        fields=['day','startTime','endTime']
