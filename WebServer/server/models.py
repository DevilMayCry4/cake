from django.db import models
from django import forms

class User(models.Model):
    username = models.CharField(max_length=200,primary_key=True)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    isSeller = models.BooleanField(default=False)
    phone = models.CharField(max_length=30)
    nickname = models.CharField(max_length=100)

class user_token(models.Model):
    username = models.CharField(max_length=200,primary_key=True)
    token = models.CharField(max_length=200)
    time = models.TimeField(blank=True, null=True)

class banner(models.Model):
    img = models.FileField(upload_to='uploads/%Y/%m/%d/')
    url = models.CharField(max_length=4000,null=True)
    show = models.BooleanField(default=True)