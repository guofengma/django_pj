from django.shortcuts import render

# Create your views here.

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Device
from .serializers import DeviceSerializer,IDCPostionSerializer

def index(request):
    return HttpResponse("Hello, world. You're at the inspection index.")

# @csrf_exempt
# def Device_list(request):
#

#http GET http://127.0.0.1:8000/inspection/getDevice/  name='Tony Deng' email='tonydeng@email.com'
#http GET http://127.0.0.1:8000/inspection/1234567/getDevice/
@api_view(['GET'])
def getDevice(request,pk):
    if request.method == "GET":
        print(pk)
        device = Device.objects.get(pk=pk)
        serializerDevice = DeviceSerializer(device)
        serializerIDCPostion = IDCPostionSerializer(device.IDCPostion)
        serializerData = dict(serializerDevice.data, **serializerIDCPostion.data)
        # print(serializerData)
        # print(serializerDevice.data.items())
        return Response(serializerData)
    # print(request.method)
    # print(JSONParser().parse(request))
    # return HttpResponse("2Hello, world. You're at the inspection getDevice.")