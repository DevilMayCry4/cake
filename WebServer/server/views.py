from django.shortcuts import render
from django.http import  HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import request
import json
from django.http import QueryDict
from server.models import User
from server.models import banner
from server.models import Good,UserTokens
from server.models import GoodImage
from server.models import get_absolute_image_url
from django.http import JsonResponse
from server.api import getLoginUser
from server.api import islogin
from server.api import isEmpty
from server.api import code_name
from server.api import msg_name
from server.api import token_name
from server.api import getLoginUserData
from server.api import isPostRequestTokenValid,PayRequest
import uuid
import time
import datetime
from server.api import getErrorJson



#首页
def home(request):
    banners = banner.objects.filter(show=True)
    user = getLoginUser(request)
    goods = Good.objects.all()
    list = []
    for good in goods:
        item = GoodItem(good)
        title = item.title
        list.append(item)
    return  render(request,"index.html",{'banners':banners,'user':getLoginUser(request),'items':list})

#注册
@csrf_exempt
def register(request):
    if request.method == 'POST':
         username = request.POST.get('username')
         email = request.POST.get('email')
         password = request.POST.get('password')
         if  isEmpty(username) or isEmpty(email) or isEmpty(password):
             string = '参数错误'
             if isEmpty(username):
                 string = '用户名不能为空'
             if isEmpty(email):
                 string = '邮箱不能为空'
             if isEmpty(password):
                 string = '密码不能为空'
                 json = {}
                 json[code_name] = 0
                 json[msg_name] = string
             return JsonResponse(json)
         else:
             users = User.objects.filter(username=username)
             if len(users) > 0:
                 return JsonResponse({code_name:0,msg_name:'用户已经存在'})
             else:
                 info = User()
                 info.username = username
                 info.nickname = request.POST.get('nickname')
                 info.email = request.POST.get('email')
                 info.password = request.POST.get('password')
                 info.save()
                 return  JsonResponse({code_name:1,msg_name:'注册成功'})
    else:
        return render(request,"register.html")


#登录
@csrf_exempt
def login(request):
    if request.method == 'POST':
         username = request.POST.get('username')
         password = request.POST.get('password')
         if isEmpty(username) or isEmpty(password):
             string = '参数错误'
             if isEmpty(username):
                 string = '用户名不能为空'
             if isEmpty(password):
                 string = '账号不能为空'
             return JsonResponse({code_name:0,msg_name:string})
         else:
             users = User.objects.filter(username=username)
             if len(users) == 0:
                 return JsonResponse({code_name:0,msg_name:'用户不存在'})
             else:
                 user = users[0]
                 if user.password != password:
                     return JsonResponse({code_name:0,msg_name:'密码错误'})
                 else:
                     token = uuid.uuid4().hex
                     model = UserTokens()
                     model.username = username
                     model.token = token
                     model.userAgent = request.META['HTTP_USER_AGENT']
                     model.time = datetime.datetime.now()
                     model.save()
                     return JsonResponse({code_name:1,token_name:token})
    else:
        return render(request,"login.html")

#上传
@csrf_exempt
def upload(request):
    user = getLoginUser(request)
    if request.method == 'POST':
        if user == None:
            return JsonResponse({code_name:0,msg_name:'token失效'})
        else:
            img = request.FILES['file_data']
            item = banner()
            item.img = img
            print (img)
            url = request.POST.get('url')
            if url != None and url.startswith('http') == False:
                url = 'http://' + url
            item.url = url
            item.save()
            return JsonResponse({code_name:1,msg_name:'上传成功'})
    else:
        if islogin(request):
            return render(request,"upload.html",getLoginUserData(request));
        else:
            return render(request,"needlogin.html",getLoginUserData(request));

#添加商品
@csrf_exempt
def addGoodItem(request):
    if request.method == 'POST':
        json = getErrorJson(request)
        if json != None:
            return json
        item = Good()
        item.title = request.POST.get('title')
        item.des =  request.POST.get('des')
        item.price = request.POST.get('price')
        item.save()
        for img in request.FILES.getlist('file_data'):
           imgItem = GoodImage()
           imgItem.good = item
           imgItem.img = img
           imgItem.save()


        return JsonResponse({code_name:1,msg_name:""})
    else:
        return  render(request,'editeitem.html',getLoginUserData(request))

#获取banners
def getBanners(request):
    banners = banner.objects.filter()
    datas = getLoginUserData(request)
    datas['banners'] = banners
    return render(request,'banners.html',datas)

def getGoodItem(request):
    idValue = request.GET.get('id')
    goods = Good.objects.filter(id=idValue)
    datas = getLoginUserData(request)
    if len(goods) >0:
        good = goods[0]
        datas['item'] = GoodItem(good)
    return render(request,'gooditem.html',datas)



class GoodItem(object):
    def __init__(self,item):
        imgs = GoodImage.objects.filter(good=item)
        self.title = item.title
        self.des = item.des
        self.price = item.price
        self.imgs = []
        self.id = item.id
        if len(imgs)>0 :
            self.img = imgs[0].img
            for img in imgs:
                self.imgs.append(img.img)
    def as_json(self,request):
        images = []
        for img in self.imgs:
            images.append(get_absolute_image_url(request,img.url))
        return dict(title=self.title,des=self.des,price=self.price,imgs=images)

