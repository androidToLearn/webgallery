
from django.db import models


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    date = models.CharField(max_length=100, default='')
    owner = models.CharField(max_length=100)
    userName = models.CharField(max_length=100, default='myname')
    accessNames = models.JSONField(default=list)
    isFavorite = models.BooleanField(default=False)
    numfile = models.IntegerField(default=0)


class User(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    color = models.CharField(max_length=30)
    mac = models.IntegerField(default=-1)
    email = models.CharField(max_length=100, default='')


class Date(models.Model):
    image = models.ImageField(upload_to='images/')
    date = models.CharField(max_length=100, default='')
    owner = models.CharField(max_length=100)
    numfile = models.IntegerField(default=0)
