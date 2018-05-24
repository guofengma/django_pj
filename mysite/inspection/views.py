# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render


import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(filename='DjangoLog.log',level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(filename='DjangoLog.log',level=logging.ERROR, format=' %(asctime)s - %(levelname)s - %(message)s')


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests,json
from os.path import sep

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Device,Event

from .serializers import DeviceSerializer,IDCPostionSerializer,EventSerializer,UserAdminSerializer


from email import encoders
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
from .settings import mailAccount,qywx
from .checkToken import checkToken

logger = logging.getLogger('django')

def index(request):
    return HttpResponse("Hello, world. You're at the inspection index.")


#http GET http://127.0.0.1:8000/inspection/Device/  name='Tony Deng' email='tonydeng@email.com'
#http GET http://127.0.0.1:8000/inspection/1234567/Device/

@api_view(['GET'])
@checkToken
def getDevice(request,pk):
    sessionid = request.COOKIES.get("sessionid")
    logger.info(sessionid + "#####扫码请求数据#######")
    if request.method == "GET":
        logger.info(sessionid + "#####设备ID：{id}#######".format(id=pk))
        device = Device.objects.get(pk=pk)
        serializerDevice = DeviceSerializer(device)
        serializerIDCPostion = IDCPostionSerializer(device.IDCPostion)
        serializerUserAdmin = UserAdminSerializer(device.userAdmins.all()[0])
        # print(serializerDevice.data)
        #
        # print(type(serializerIDCPostion.data))
        # print(type(serializerUserAdmin.data))

        serializerData = dict(dict(serializerDevice.data, **serializerIDCPostion.data),**serializerUserAdmin.data)
        print(serializerData)
        # print(dict(serializerDevice.data.items() + serializerIDCPostion.data.items()))
        # print(serializerDevice.data.items())
        return Response(serializerData)
    # print(request.method)
    # print(JSONParser().parse(request))
    # return HttpResponse("2Hello, world. You're at the inspection getDevice.")

#http -f POST http://127.0.0.1:8000/inspection/Event/ name='John Smith' file@./123.png,./456.png
@api_view(['POST'])
@checkToken
def postEvent(request,pk):
    sessionid = request.COOKIES.get("sessionid")
    logger.info(sessionid + "#####生成故障#######")
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
            # server.set_debuglevel(1)
            server.login(from_addr, password)
            server.sendmail(from_addr, to_addr, msg.as_string())
            server.quit()

        def SendWarningWeiXin(event):
            touser = ''
            message = '''
  您的设备%(model)s，序列号%(serialNumber)s
  位于%(IDCPostionName)s机房,%(rackPostion)s机架（机房联系电话：%(TelephoneNumber)s，地址：%(IDCPostionAddress)s）
  在%(EventDate)s发生故障，发现人%(reportUserInfo)s，申告诉内容：
      %(description)s
            '''%{'model':event.model,'serialNumber':event.Device.serialNumber,'rackPostion':event.rackPostion,'IDCPostionName':event.Device.IDCPostion.IDCPostionName,
                 'TelephoneNumber':event.Device.IDCPostion.TelephoneNumber,'IDCPostionAddress':event.Device.IDCPostion.IDCPostionAddress,
                 'EventDate':event.EventDate,'reportUserInfo':event.reportUserInfo,'description':event.description
                 }
            for userAdmin in event.Device.userAdmins.all():
                if userAdmin.wx_id:
                    if touser :
                        touser = touser+'|'+userAdmin.wx_id
                    else:
                        touser = userAdmin.wx_id
                logging.debug(touser)
            if touser :
                session = requests.session()
                QywxUrl = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid="+qywx.corpid+"&corpsecret="+qywx.corpsecret
                logging.debug(QywxUrl)
                logging.debug(message)
                r = session.get(QywxUrl, verify=False)
                token = json.loads(r.text)
                data = json.dumps({
                    "touser": touser,
                    "toparty": "",
                    "totag": "",
                    "msgtype": "text",
                    "agentid": 1000003,
                    "text": {
                        "content": message
                    },
                    "safe": 0
                })
                r = session.post(
                    "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + token['access_token'], data=data)

                upload_img = {
                    'access_token': token['access_token'],
                    'type': 'image'
                }

                if event.imageOne:
                    with event.imageOne.open() as image:
                        files = {'file': (image.name.split(sep)[-1], image)}
                        logging.debug(files)
                        urlupload = 'https://qyapi.weixin.qq.com/cgi-bin/media/upload'
                        r2 = requests.post(url=urlupload, params=upload_img, files=files)
                        media_id = json.loads(r2.text)
                        logging.debug(media_id)
                    data = json.dumps({
                        "touser": touser,
                        "toparty": "",
                        "totag": "",
                        "msgtype": "image",
                        "agentid": 1000003,
                        "image": {
                            "media_id": media_id['media_id']
                        },
                        "safe": 0
                    })
                    r = session.post(
                        "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + token['access_token'],
                        data=data)




        if pk == '':
            serializer = EventSerializer(data=request.data)
            # 生产一个event，并返回一个eventID
            print(request.data)
            print(serializer)
            print(serializer.is_valid())
            #else要报个错误
            if serializer.is_valid():
                serializer.save()
                logger.info(sessionid + "#####生成故障ID:{id}#######".format(id=serializer.data['id']))
                # logging.debug(serializer.data['id'])
                return Response(serializer.data)
        else:
            event = Event.objects.get(id = pk)

            # logging.debug(request.META.get('CONTENT_TYPE'))
            # logging.debug('multipart/form-data;'in request.META.get('CONTENT_TYPE'))
            if('multipart/form-data;'in request.META.get('CONTENT_TYPE')):
                event.imageOne = request.FILES.get("imageOne")
                event.save()
            try:
                logger.info(sessionid + "#####故障ID:{id}，发邮件了#######".format(id=pk))
                SendWarningMail(event)
            except  Exception as e:
                logger.error(sessionid + "#####发邮件失败了#######")
                logger.error(e)
            try:
                logger.info(sessionid + "#####故障ID:{id}，发微信了#######".format(id=pk))
                SendWarningWeiXin(event)
            except  Exception as e:
                logger.error(sessionid + "#####发微信失败了#######")
                logger.error(e)

            # print(request.data)
            # serializer = EventSerializer(event,data=dict(request.data))
            # print(serializer)
            # print(serializer.is_valid())
            return HttpResponse("OK")
            # device = Device.objects.get(pk=pk)






