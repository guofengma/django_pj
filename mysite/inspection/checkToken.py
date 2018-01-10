from django.http import HttpResponse
from functools import wraps
import hashlib
from .settings import tokenKey
def checkToken(f):
    @wraps(f)
    def decorated(request,*args, **kwargs):
        # print('checkToken')
        # print(request.META)
        print('request_token:'+request.META.get('HTTP_TOKEN'))
        hash = hashlib.md5()
        hash.update(tokenKey.key.encode('utf-8'))
        print('MD5:'+hash.hexdigest())
        if hash.hexdigest() == request.META.get('HTTP_TOKEN'):
            return f(request,*args, **kwargs)
        else:
            return HttpResponse(status=403)
    return decorated