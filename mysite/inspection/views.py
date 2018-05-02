# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render


import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Device,Event

from .serializers import DeviceSerializer,IDCPostionSerializer,EventSerializer


from email import encoders
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
from .settings import mailAccount
from .checkToken import checkToken



def index(request):
    return HttpResponse("Hello, world. You're at the inspection index.")


#http GET http://127.0.0.1:8000/inspection/Device/  name='Tony Deng' email='tonydeng@email.com'
#http GET http://127.0.0.1:8000/inspection/1234567/Device/

@api_view(['GET'])
@checkToken
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
@checkToken
def postEvent(request,pk):
    if request.method == "POST":
        def SendWarningMail(event):
            msgStr = ''
            to_addr = []
            # print(event.Device)
            # print(event.Device.model)
            # print(event.Device.userAdmins.all())
            print('#'*20)
            for userAdmin in event.Device.userAdmins.all():
                to_addr.append(userAdmin.email)
                if msgStr == '':
                    msgStr = '<html><body><p>Hello, ' + userAdmin.Name
                else:
                    msgStr = msgStr + ', ' +userAdmin.Name
            msgStr = msgStr + ': </p>' + '''
  <p>您的设备%(model)s，序列号%(serialNumber)s
  位于%(IDCPostionName)s机房,%(rackPostion)s机架（机房联系电话：%(TelephoneNumber)s，地址：%(IDCPostionAddress)s）
  在%(EventDate)s发生故障，发现人%(reportUserInfo)s，申告诉内容：</p>
      <p>%(description)s</p>
      <p><img src="cid:image1"></p></body></html>
            '''%{'model':event.model,'serialNumber':event.Device.serialNumber,'rackPostion':event.rackPostion,'IDCPostionName':event.Device.IDCPostion.IDCPostionName,
                 'TelephoneNumber':event.Device.IDCPostion.TelephoneNumber,'IDCPostionAddress':event.Device.IDCPostion.IDCPostionAddress,
                 'EventDate':event.EventDate,'reportUserInfo':event.reportUserInfo,'description':event.description
                 }
            # print(to_addr)
            # print(msgStr)

            from_addr = mailAccount.mailAddress
            password = mailAccount.password
            smtp_server = mailAccount.smtp_server



            msg = MIMEMultipart()
            msg['From'] = from_addr
            msg['To'] = ''
            for s in to_addr:
                if msg['To'] == '':
                    msg['To'] = s
                else:
                    msg['TO'] = msg['TO'] + ',' + s
            msg['Subject'] = Header('这是来自上海电信现场报障系统的事件通知，事件单号%s' % event.id, 'utf-8').encode()
            # 邮件正文是MIMEText:
            msg.attach(MIMEText(msgStr, 'html', 'utf-8'))

            #如果有图片就加图片
            # logging.debug(event.imageOne)
            # logging.debug(event.imageTwo)
            if event.imageOne :
                with event.imageOne.open() as image:
                    img = MIMEImage(image.read())
                # img.add_header('Content-Disposition', 'attachment', filename='test.png')
                img.add_header('Content-ID', '<image1>')
                img.add_header('X-Attachment-Id', 'image1')
                # img.add_header('Content-transfer-encoding', 'base64')
                msg.attach(img)

            server = smtplib.SMTP(smtp_server, 25)
            server.set_debuglevel(1)
            server.login(from_addr, password)
            server.sendmail(from_addr, to_addr, msg.as_string())
            server.quit()

        def SendWarningWeiXin(event):
            pass

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
            logging.debug(request.META.get('CONTENT_TYPE'))
            logging.debug('multipart/form-data;'in request.META.get('CONTENT_TYPE'))
            if('multipart/form-data;'in request.META.get('CONTENT_TYPE')):
                event.imageOne = request.FILES.get("imageOne")
                event.save()
            SendWarningMail(event)
            # print(request.data)
            # serializer = EventSerializer(event,data=dict(request.data))
            # print(serializer)
            # print(serializer.is_valid())
            return HttpResponse("OK")
            # device = Device.objects.get(pk=pk)






