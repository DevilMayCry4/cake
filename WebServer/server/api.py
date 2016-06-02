from django.shortcuts import render
from django.http import  HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import request
import json
from django.http import QueryDict
from server.models import User,Good,GoodImage
from server.models import UserTokens
from server.models import banner,Order
from django.http import JsonResponse
from django.core import serializers
import time
import os

token_name = 'token'
code_name = 'code'
msg_name = 'msg'
PingPP_APPKey = 'app_qX98mLCSu98KPSyL'

currentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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
            tokens = UserTokens.objects.filter(token=value)
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
            tokens = UserTokens.objects.filter(token=token)
            return len(tokens) != 0
    return False


#判断函数
def islogin(request):
    return getLoginUser(request) != None

def isEmpty(string):
    return  string == None or len(string) == 0

def getBoolValue(string):
    return string == True or string == 'true'

def getLoginUserData(request):
    user = getLoginUser(request)
    return {'user':getLoginUser(request)}

def getErrorJson(request):
    if isPostRequestTokenValid(request) == False:
           return JsonResponse({code_name:0,msg_name:'登录已失效、请登录'})
    return None

def createPayOrder(request):
    if islogin(request):
       if request.method == 'POST':
          pay = PayRequest(request)
          return pay.createOrderId()
       return createErrorJson('请用post方法')
    return createErrorJson('请登录')

def createErrorJson(msg):
    return JsonResponse({code_name:0,msg_name:msg})



#app api
def appGetHome(request):
    from server.views import GoodItem
    banners = banner.objects.filter(show=True)
    bannerList = []
    for b in banners:
        bannerList.append(b.as_json(request))
    user = getLoginUser(request)
    goods = Good.objects.all()
    list = []
    for good in goods:
        item = GoodItem(good)
        title = item.title
        list.append(item.as_json(request))
    return JsonResponse({code_name:1,'banners':bannerList,'items':list})

class PayRequest(object):
    def __init__(self,request):
        self.request = request

    def createOrderId(self):
        if islogin(self.request):
            user = getLoginUser(self.request)
            orders = Order.objects.filter(user=user)
            return self.GetNowTime()+ str(len(orders))

        return None
    def GetNowTime(self):
        return time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))

    def getCharge(self):
        goodid = self.request.POST.get('goodid')
        paytype = self.request.POST.get('paytype')
        if goodid == None or paytype == None:
            return createErrorJson('参数不正确')
        orderid = self.createOrderId()
        if orderid == None:
            return {code_name:0,msg_name:'无法创建订单'}

        params = {}
        params['order_no'] = orderid
        params['app'] = dict(id=PingPP_APPKey)
        params['currency'] = 'cny'
        params['subject'] = 'Your Subject'
        params['body'] = 'Your Body'
        params['channel'] = paytype
        params['amount'] = 1100
        params['extra'] = dict(nick_name='Nick Name', send_name='Send Name')
        params['recipient'] = 'Openid'
        params['description'] = 'Your Description'
        pingpp.api_key = 'sk_test_uHafrLbD0mfPf9GKqDa1aL84'
        pingpp.private_key_path = currentDir + '/server/RSACert/rsa_private_key.pem'
        response_redenvelope = pingpp.RedEnvelope.create(api_key=pingpp.api_key,
                                                     **params)
        print ('Response_redenvelope: ' + str(response_redenvelope))
