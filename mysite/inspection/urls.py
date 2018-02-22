from django.conf.urls import url
from . import views
app_name = 'inspection'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^Device/(?P<pk>[A-Za-z0-9_\-]+)/$', views.getDevice, name='getDevice'),
    url(r'^Event/(?P<pk>[0-9]*)/?$', views.postEvent, name='postEvent'),
]