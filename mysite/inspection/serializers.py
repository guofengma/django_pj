#!/usr/bin/env python3

from rest_framework import serializers
from .models import *

class IDCPostionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IDCPostion
        fields = ('IDCPostionName','TelephoneNumber','IDCPostionAddress')

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('serialNumber','model','rackPostion')

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id','EventDate','description','Device','imageOne','imageTwo','imageThree')