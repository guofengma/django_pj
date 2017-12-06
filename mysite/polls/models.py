# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Question(models.Model):
    question_test = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


class IDCPostion(models.Model):
    IDCPostionName = models.CharField(max_length=20)
    TelephoneNumber = models.CharField(max_length=12)
    IDCPostionAddress = models.CharField(max_length=100)

class userAdmin(models.Model):
    Depertment = models.CharField(max_length=100)
    email = models.EmailField()
    TelephoneNumber = models.CharField(max_length=12)


class Device(models.Model):
    serialNumber = models.CharField(max_length=50,primary_key=True)
    model = models.CharField(max_length=100)
    rackPostion = models.CharField(max_length=10)
    IDCPostion = models.ForeignKey(IDCPostion)
    userAdmins = models.ManyToManyField(userAdmin)


class Event(models.Model):
    EventDate = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    imageOne = models.ImageField()
    imageTwo = models.ImageField()
    imageThree = models.ImageField()
    Device = models.ForeignKey(Device)





# Create your models here.
