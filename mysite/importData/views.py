from django.shortcuts import render
import logging
import re

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from inspection.models import IDCPostion,userAdmin,Device
from django.shortcuts import get_object_or_404, render
# from django.views import generic
from django.urls import reverse
from .models import DataPostForm,DataPostFormPlus
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import pandas as pd

logger = logging.getLogger('django')

@login_required
def index(request):
    # print(request.user.is_authenticated)
    try:
        message = request.GET['message']
    except (KeyError):
        message = None
    IDCPostionlist = IDCPostion.objects.order_by('id')
    userAdminlist = userAdmin.objects.order_by('id')
    return render(request, 'importData/index.html', {
        'IDCPostionlist': IDCPostionlist ,'userAdminlist':userAdminlist,'message':message,
        'form':DataPostForm(),'formPlus':DataPostFormPlus()
    })

@login_required
def IDCPostionDetail(request,IDCPostionID):
    IDCPostion_id = get_object_or_404(IDCPostion,pk=IDCPostionID)
    return render(request, 'importData/IDCPostionDetail.html', {'IDCPostion': IDCPostion_id})

@login_required
def userAdminDetail(request,userAdminID):
    userAdmin_id = get_object_or_404(userAdmin,pk=userAdminID)
    return render(request, 'importData/userAdminDetail.html', {'userAdmin': userAdmin_id})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('importData:index'))

#
# class IDCPostionDetail(generic.DetailView):
#     model = IDCPostion
#     template_name = 'importData/IDCPostionDetail.html'
#     # HttpResponse("Hello!")
#
# class userAdminDetail(generic.DetailView):
#     model = userAdmin
#     template_name = 'importData/userAdminDetail.html'

@login_required
def dataAction(request):
    sessionid = request.COOKIES.get("sessionid")
    logger.info(sessionid+"#####导入数据（3列的那种）#######")
    message = ''
    try:
        # 第一次检验数据，检验数据大小，检验文件后缀名
        # logger.debug(request.FILES['dataFile'].size)
        # logger.debug(request.FILES['dataFile'].name,type(request.FILES['dataFile'].name))
        # logger.debug(re.match(r'.+\.xls$',request.FILES['dataFile'].name) == None)
        logger.info(sessionid+"#####上传文件名：{filename}######".format(filename=request.FILES['dataFile'].name))
        if request.FILES['dataFile'].size > 500000:
            message = "文件大小需要小于500K"
            raise Exception(message)
        if re.match(r'.+\.xls$',request.FILES['dataFile'].name) == None:
            message = "文件必须是xls，文件格式无效"
            raise Exception(message)
        form = DataPostForm(request.POST, request.FILES)
        if form.is_valid():
            dataPost = form.save(commit=False)
            dataPost.updataUser = request.user
            dataPost.save()
            dataPost.userAdmins.add(*userAdmin.objects.filter(id__in=request.POST['userAdmins']))
            logger.info(sessionid+"#####上传者:{updataUser}#####".format(updataUser=dataPost.updataUser))
            # logger.debug(dataPost)
            logger.info(dataPost.dataFile)
            try:
                data = pd.read_excel(dataPost.dataFile)
            except Exception as e:
                logger.info('Error:', e)
                message = 'excel无法打开，数据文件格式错误'
                raise Exception(message)
            # 第二次检验数据，是不是3列，列的名称对不对，是否包含空置
        if data.shape[1] != 3:
            message = '导入数据不为3列，格式错误，请参照数据样例！'
            raise Exception(message)
        if not (data.columns[0]=='serialNumber' and data.columns[1]=='model' and data.columns[2] == 'rackPostion'):
            message = '3列必须为“serialNumber，model，rackPostion”，格式错误，请参照数据样例！'
            raise Exception(message)
        if True in data.isnull().values:
            message = '上传数据中不能包含空置！请检查！'
            raise Exception(message)
        logger.info(sessionid+"#####数据校验通过#######")
        for i in range(data.shape[0]):
            d = Device(serialNumber=data['serialNumber'][i], model=data['model'][i], rackPostion=data['rackPostion'][i],
                    IDCPostion=dataPost.IDCPostion)
            d.save()
            d.userAdmins.clear()
            d.userAdmins.add(*dataPost.userAdmins.all())
        logger.info(sessionid+"#####数据导入成功#######")

        message = '数据导入成功'
    except  Exception as e:
        logger.error(sessionid+"#####数据导入失败#######")
        logger.error(message)
    finally:
        if not message:
            message = '未知错误'
            logger.error(sessionid+"#####未知错误#######")
        url = reverse('importData:index') + '?' + 'message=' + message
        # logger.debug(url)
        return HttpResponseRedirect(url)

@login_required
def dataActionPlus(request):
    sessionid = request.COOKIES.get("sessionid")
    # logger.debug(request.user.username)
    logger.info(sessionid+"#####导入数据（5列的那种）#######")
    message = ''
    try:
        # 第一次检验数据，检验数据大小，检验文件后缀名
        # logger.debug('#'*50)
        # logger.debug(request)
        # logger.debug(request.FILES['dataFile'])
        # logger.debug(re.match(r'.+\.xls$',request.FILES['dataFile'].name) == None)
        logger.info(sessionid+"#####上传文件名：{filename}######".format(filename=request.FILES['dataFile'].name))
        if request.FILES['dataFile'].size > 500000:
            message = "文件大小需要小于500K"
            raise Exception(message)
        if re.match(r'.+\.xls$', request.FILES['dataFile'].name) == None:
            message = "文件必须是xls，文件格式无效"
            raise Exception(message)
        form = DataPostFormPlus(request.POST, request.FILES)
        if form.is_valid():
            dataPostPlus = form.save(commit=False)
            dataPostPlus.updataUser = request.user
            # logger.debug(dataPostPlus.updataUser)
            dataPostPlus.save()
            # logger.debug('dataPostPlus',dataPostPlus)
            # logger.debug(form)
            logger.info(sessionid+"#####上传者:{updataUser}#####".format(updataUser=dataPostPlus.updataUser))
            try:
                data = pd.read_excel(dataPostPlus.dataFile)
                # logger.debug(data)
            except Exception as e:
                # logger.debug('Error:', e)
                message = 'excel无法打开，数据文件格式错误'
                raise Exception(message)
                # 第二次检验数据，是不是3列，列的名称对不对，是否包含空置
        if data.shape[1] != 5:
            message = '导入数据不为5列，格式错误，请参照数据样例！'
            raise Exception(message)
        # logger.debug(data.columns)
        if not (data.columns[0] == 'serialNumber' and data.columns[1] == 'model' and data.columns[2] == 'rackPostion'
                and data.columns[3] == 'IdcPostions' and data.columns[4] == 'UserAdmins'):
            message = '5列必须为“serialNumber，model，rackPostion，IdcPostions，UserAdmins”，格式错误，请参照数据样例！'
            raise Exception(message)
        if True in data.isnull().values:
            message = '上传数据中不能包含空置！请检查！'
            raise Exception(message)
        logger.info(sessionid+"#####数据校验通过#######")
        for i in range(data.shape[0]):
            d = Device(serialNumber=data['serialNumber'][i], model=data['model'][i], rackPostion=data['rackPostion'][i],
                       IDCPostion=IDCPostion.objects.get(id=data['IdcPostions'][i]))
            d.save()
            d.userAdmins.clear()
            userAdminsQuerySet =  userAdmin.objects.filter(id__in=str(data['UserAdmins'][i]).split(';'))
            # logger.debug(userAdminsQuerySet)
            d.userAdmins.add(*userAdminsQuerySet)
            # logger.debug(i)
        message = '数据导入成功'
        logger.info(sessionid+"#####数据导入成功#######")
    except  Exception as e:
        logger.error(sessionid+"#####数据导入失败#######")
        logger.error(message)
        logger.error(e)
    finally:
        if not message:
            message = '未知错误'
            logger.error(sessionid+"#####未知错误#######")
        url = reverse('importData:index') + '?' + 'message=' + message
        # logger.debug(url)
        return HttpResponseRedirect(url)





    #     d = Device(serialNumber=data['serialNumber'][0], model=data['model'][0], rackPostion=data['rackPostion'][0],
    #                IDCPostion=dP.IDCPostion, userAdmins=dP.userAdmins.all())
    #     d.save()
    #     d.userAdmins.add(*dP.userAdmins.all())





