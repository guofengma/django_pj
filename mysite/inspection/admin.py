from django.contrib import admin
from .models import *

class EventAdmin1(admin.ModelAdmin):
    list_display = ('id','IDCPostionName')


class EventAdmin2(admin.ModelAdmin):
    list_display = ('id','Name')

class EventAdmin3(admin.ModelAdmin):
    list_display=('id', 'EventDate','reportUserInfo', 'Device','model','rackPostion','description', 'imageOne')
# Register your models here.


admin.site.register(IDCPostion,EventAdmin1)
admin.site.register(userAdmin,EventAdmin2)
admin.site.register(Device)
admin.site.register(Event,EventAdmin3)


