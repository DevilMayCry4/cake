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

token_name = 'token'
code_name = 'code'
msg_name = 'msg'

@csrf_exempt
def deleteBanner(request):
    if request.method == 'POST':
        if isPostRequestTokenValid(request) == False:
           return JsonResponse({code_name:0,msg_name:'登录已失效、请登录'})
        itemId = request.POST.get('id')
        if itemId != None:
            banners = banner.objects.filter(id=itemId)
            if len(banners) != 0:
                banners[0].delete()
                return JsonResponse({code_name:1,msg_name:'删除成功'})

        return JsonResponse({code_name:0,msg_name:"参数错误"})
    else:
        return JsonResponse({code_name:0,msg_name:"请使用post"})


@csrf_exempt
def updateBanner(request):
    if request.method == 'POST':
        if isPostRequestTokenValid(request) == False:
           return JsonResponse({code_name:0,msg_name:'登录已失效、请登录'})
        itemId = request.POST.get('id')
        show = request.POST.get('show')
        if itemId != None and show != None:
            banners = banner.objects.filter(id=itemId)
            if len(banners) != 0:
                banners[0].show = getBoolValue(show)
                banners[0].save()
                return JsonResponse({code_name:1,msg_name:'更新成功'})

        return JsonResponse({code_name:0,msg_name:"参数错误"})
    else:
        return JsonResponse({code_name:0,msg_name:"请使用post"})

#获取当前登录的用户
def getLoginUser(request):
    if token_name in request.COOKIES:
        value = request.COOKIES[token_name]
        if len(value) != 0:
            tokens = user_token.objects.filter(token=value)
            if len(tokens) != 0:
                token = tokens[0]
                users = User.objects.filter(username=token.username)
                if len(users) > 0:

                    return users[0]

    return None

def isPostRequestTokenValid(request):
    if request.method == 'POST':
        if token_name in request.POST:
            token = request.POST.get(token_name)
            tokens = user_token.objects.filter(token=token)
            return len(tokens) != 0
    return False

#判断函数
def islogin(request):
    return getLoginUser(request) != None

def isEmpty(string):
    return  string == None or len(string) == 0

def getBoolValue(string):
    return string == True or string == 'true'