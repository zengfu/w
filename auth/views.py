# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.views.decorators.csrf import csrf_exempt
import json
import httplib

from django.shortcuts import render

# Create your views here.
def hello(request):
    return HttpResponse("Hello world")

def index(request):
    return render(request, "index.html")
def mqtt(request):
    return render(request,"mqtt.html")

@csrf_exempt
def login_view(request):
    username=request.POST['username']
    password=request.POST['password']
    print username,password
    user=authenticate(username=username,password=password)
    res=0
    if user is not None:
        if user.is_active:
            login(request,user)
            username=user.username
        else:
            res=1

    else:
        res=1
    result_json = {'result': res,'username':username}
    return HttpResponse(json.dumps(result_json), content_type='application/json')
def logout_view(request):
    res=0
    if request.user.is_authenticated():
        logout(request)
        res=0
    else:
        res=1
    result_json={'result':res}
    return HttpResponse(json.dumps(result_json),content_type='application/json')
def mysession(request):
    res = 0
    if request.user.is_authenticated():
        res = 0
        result_json = {'result': res,'username':request.user.username}
    else:
        res = 1
        result_json = {'result': res}
    print json.dumps(result_json)
    return HttpResponse(json.dumps(result_json), content_type='application/json')
def getmqttclient(request):
    conn=httplib.HTTPConnection("127.0.0.1",1885)
    conn.request("GET","/api/allmqtt")
    res=conn.getresponse()
    data=res.read()
    print data
    return HttpResponse(data)
