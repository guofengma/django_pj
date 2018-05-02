from django.urls import path

from . import views
app_name = 'importData'
urlpatterns = [
    path('', views.index, name='index'),
    path('IDCPostion/<int:IDCPostionID>/', views.IDCPostionDetail, name='IDCPostionDetail'),
    path('userAdmin/<int:userAdminID>/', views.userAdminDetail, name='userAdminDetail'),
    # path('IDCPostion/<int:pk>/', views.IDCPostionDetail.as_view(), name='IDCPostionDetail'),
    # path('userAdmin/<int:pk>/', views.userAdminDetail.as_view(), name='userAdminDetail'),
    path('dataAction/', views.dataAction, name='dataAction'),
    path('dataActionPlus/', views.dataActionPlus, name='dataActionPlus'),
    path('logout/',views.logout_view, name='logout')
]