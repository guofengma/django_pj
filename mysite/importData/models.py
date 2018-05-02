from django.db import models
from django import forms
# Create your models here.
from inspection.models import IDCPostion,userAdmin
from django.contrib.auth.models import User



class DataPost(models.Model):
    # IDCPostionlist = IDCPostion.objects.order_by('id')
    # choices = []
    # for IDCPostion in IDCPostionlist:
    #     choices.append((IDCPostion.id, IDCPostion.IDCPostionName))
    # DataIDCPostion = models.CharField(max_length=20,choices=choices)
    # title = models.CharField(max_length=150)
    dataFile = models.FileField(upload_to='uploads/',blank=True)
    IDCPostion = models.ForeignKey(IDCPostion,on_delete=models.CASCADE)
    userAdmins = models.ManyToManyField(userAdmin)
    updataUser = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True,)

class DataPostForm(forms.ModelForm):
    # title = forms.CharField(max_length=150)
    class Meta:
        model = DataPost
        # fields = '__all__'
        exclude = ('updataUser',)

class DataPostPlus(models.Model):
    dataFile = models.FileField(upload_to='uploads/', blank=True)
    updataUser = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, )

class DataPostFormPlus(forms.ModelForm):
    class Meta:
        model = DataPostPlus
        # fields = '__all__'
        exclude = ('updataUser',)