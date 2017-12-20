from django.conf.urls import url
from . import views
app_name = 'inspection'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>[0-9]+)/getDevice/$', views.getDevice, name='getDevice')
]