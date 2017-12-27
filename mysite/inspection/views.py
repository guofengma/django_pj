from django.shortcuts import render

# Create your views here.

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Device,Event
from .serializers import DeviceSerializer,IDCPostionSerializer,EventSerializer

def index(request):
    return HttpResponse("Hello, world. You're at the inspection index.")

# @csrf_exempt
# def Device_list(request):
#

#http GET http://127.0.0.1:8000/inspection/Device/  name='Tony Deng' email='tonydeng@email.com'
#http GET http://127.0.0.1:8000/inspection/1234567/Device/
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

#http -f POST http://127.0.0.1:8000/inspection/Event/ name='John Smith' file@./123.png,./456.png
@api_view(['POST'])
def postEvent(request,pk):
    if request.method == "POST":
        if pk == '':
            serializer = EventSerializer(data=request.data)
            # 生产一个event，并返回一个eventID
            print(request.data)
            print(serializer)
            print(serializer.is_valid())
            #else要报个错误
            if serializer.is_valid():
                serializer.save()
                print(serializer.data['id'])
                return Response(serializer.data)
        else:
            event = Event.objects.get(id = pk)
            event.imageOne = request.FILES.get("imageOne")
            event.save()
            # print(request.data)
            # serializer = EventSerializer(event,data=dict(request.data))
            # print(serializer)
            # print(serializer.is_valid())
            return HttpResponse("test")
            # device = Device.objects.get(pk=pk)





