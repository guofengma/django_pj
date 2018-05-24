import requests
import json
from os.path import sep

session = requests.session()
loginurl = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=wwc4c982387d38486f&corpsecret=HxZNSzVC52nDhqMYIDxhzxZOe-2v8Iw_pl04qfQFKf0"
r = session.get(loginurl,verify=False)
token = json.loads(r.text)
data = json.dumps({
    "touser" : "DuDu",
    "toparty" : "",
    "totag" : "",
    "msgtype" : "text",
    "agentid" : 1000003,
    "text" : {
        "content" : "message"
    },
    "safe":0
})
r = session.post("https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + token['access_token'], data=data)

######################################################################################################################################

session = requests.session()
loginurl = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=wwc4c982387d38486f&corpsecret=HxZNSzVC52nDhqMYIDxhzxZOe-2v8Iw_pl04qfQFKf0"
r = session.get(loginurl,verify=False)
token = json.loads(r.text)
upload_img={
    'access_token' : token['access_token'],
    'type' : 'image'
}

f = open('/home/wanshuxiao/workspace/django_pj/mysite/uploads/test1.png','rb')
files = {'file': (f.name.split(sep)[-1], f)}


urlupload='https://qyapi.weixin.qq.com/cgi-bin/media/upload'
r2 = requests.post(url=urlupload,params=upload_img,files=files)

media_id = json.loads(r2.text)

data = json.dumps({
    "touser" : "DuDu",
    "toparty" : "",
    "totag" : "",
    "msgtype" : "image",
    "agentid" : 1000003,
    "image" : {
        "media_id" : media_id['media_id']
    },
    "safe":0
})
r = session.post("https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + token['access_token'], data=data)