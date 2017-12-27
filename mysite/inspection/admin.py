from django.contrib import admin
from .models import *

class EventAdmin(admin.ModelAdmin):
    list_display=('id', 'EventDate', 'Device','description', 'imageOne')
# Register your models here.

admin.site.register(IDCPostion)
admin.site.register(userAdmin)
admin.site.register(Device)
admin.site.register(Event,EventAdmin)


