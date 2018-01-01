from django.db import models

# Create your models here.

from django.db import models

class IDCPostion(models.Model):
    IDCPostionName = models.CharField(max_length=20)
    TelephoneNumber = models.CharField(max_length=12)
    IDCPostionAddress = models.CharField(max_length=100)
    def __str__(self):
        return  self.IDCPostionName

class userAdmin(models.Model):
    Name = models.CharField(max_length=10)
    Depertment = models.CharField(max_length=100)
    email = models.EmailField()
    TelephoneNumber = models.CharField(max_length=12)
    def __str__(self):
        return self.Name


class Device(models.Model):
    serialNumber = models.CharField(max_length=50,primary_key=True)
    model = models.CharField(max_length=100)
    rackPostion = models.CharField(max_length=10)
    IDCPostion = models.ForeignKey(IDCPostion,on_delete=models.CASCADE)
    userAdmins = models.ManyToManyField(userAdmin)
    def __str__(self):
        return self.serialNumber


class Event(models.Model):
    EventDate = models.DateTimeField(auto_now_add=True)
    model = models.CharField(max_length=100,blank=True)
    rackPostion = models.CharField(max_length=10,blank=True)
    description = models.TextField(blank=True)
    reportUserInfo = models.CharField(max_length=100,blank=True)
    imageOne = models.ImageField(upload_to='uploads/',blank=True)
    imageTwo = models.ImageField(upload_to='uploads/',blank=True)
    imageThree = models.ImageField(upload_to='uploads/',blank=True)
    Device = models.ForeignKey(Device,on_delete=models.CASCADE)
    def __str__(self):
        return self.description
