#!/usr/bin/env python3

from rest_framework import serializers
from .models import *

class IDCPostionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IDCPostion
        fields = ('IDCPostionName','IDCPostionAddress')

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('serialNumber','model','rackPostion')

class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = userAdmin
        fields = ('Name','TelephoneNumber')

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id','EventDate','reportUserInfo', 'model','rackPostion','description','Device','imageOne','imageTwo','imageThree')