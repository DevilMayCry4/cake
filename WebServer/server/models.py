from django.db import models
from django import forms
from WebServer.settings import MEDIA_URL


def get_absolute_image_url(request,url):
    return  request.build_absolute_uri(url)

class User(models.Model):
    username = models.CharField(max_length=200,primary_key=True)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    isSeller = models.BooleanField(default=False)
    phone = models.CharField(max_length=30)
    nickname = models.CharField(max_length=100)
    avatar = models.FileField(upload_to='uploads/%Y/%m/%d/',null = True, blank = True)
    isAdmin = models.BooleanField(default=False)

class UserTokens(models.Model):
    username = models.CharField(max_length=200)
    token = models.CharField(max_length=200,primary_key=True)
    time = models.DateTimeField(blank=True, null=True,auto_now=True)
    userAgent = models.CharField(max_length=400,default='')

class banner(models.Model):
    img = models.FileField(upload_to='uploads/%Y/%m/%d/')
    url = models.CharField(max_length=4000,null=True)
    show = models.BooleanField(default=True)
    def as_json(self,request):
        return dict(img=get_absolute_image_url(request,self.img.url),url=self.url,show=self.show)

class Good(models.Model):
    title = models.CharField(blank=True,null=True,max_length=200)
    price = models.CharField(blank=True,null=True,max_length=100)
    des = models.TextField(blank=True,null=True)
    def as_json(self):
        return dict(title=self.title,price=self.price,des=self.des)

class GoodImage(models.Model):
    good = models.ForeignKey(Good,default=None)
    img = models.FileField(upload_to='uploads/%Y/%m/%d/',null = True, blank = True)

class Order(models.Model):
    good = models.ForeignKey(Good,default=None)
    user = models.ForeignKey(User,default=None)
    date = models.DateTimeField()



