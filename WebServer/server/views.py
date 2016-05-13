from django.shortcuts import render
from django.http import  HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import request
import json
from django.http import QueryDict
from server.models import User
from server.models import  user_token
from server.models import banner
from django.http import JsonResponse
from server.api import getLoginUser
from server.api import islogin
from server.api import isEmpty
from server.api import code_name
from server.api import msg_name
from server.api import token_name
import uuid



#首页
def home(request):
    banners = banner.objects.filter(show=True)
    user = getLoginUser(request)
    return  render(request,"index.html",{'banners':banners,'user':getLoginUser(request)})

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
                     model = user_token()
                     model.username = username
                     model.token = token
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
            url = request.POST.get('url')
            if url != None and url.startswith('http') == False:
                url = 'http://' + url
            item.url = url
            item.save()
            return JsonResponse({code_name:1,msg_name:'上传成功'})
    else:
        if islogin(request):
            return render(request,"upload.html");
        else:
            return render(request,"needlogin.html");

#添加商品
@csrf_exempt
def addGoodItem(request):
    return  render(request,'editeitem.html')

#获取banners
def getBanners(request):
    banners = banner.objects.filter()
    return render(request,'banners.html',{'banners':banners});

