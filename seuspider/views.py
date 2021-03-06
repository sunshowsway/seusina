#/usr/bin/python3.6
from django.shortcuts import render
from django.views.generic import View
from  seuspider.models import *
from django.http import HttpResponseRedirect,HttpResponse
import json,redis,time
from django.core.urlresolvers import reverse
# Create your views here.

import requests,json

class sina(View):

    def get(self,request):
        return  render(request,"personalweibo.html",{"message":""})

    def post(self,request):
        cookie = request.POST.get("cookie", "")
        url = request.POST.get("url", "")
        data = {"project": "sina", "spider": "sinaspider", "cookie": cookie, "url": url}
        result = requests.post("http://120.78.196.125/schedule.json", data=data)
        result = json.loads(result.text)
        jobid = result["jobid"]
        if result["status"]=='ok':
            return render(request, "result_sina.html", {'cookie': cookie,'jobid':jobid})
        else:
            return  render(request,"personalweibo.html",{"message":"爬虫启动失败"})

class result(View):
    def post(self,request):
        res={}
        r = redis.Redis(host='120.78.196.125', port=6379)

        cookie = request.POST.get("cookie","")
        print(cookie)
        try:
            timeVal=r.lpop(cookie+'datetime')
            likenum=r.lpop(cookie+'likenum')
            repeatnum = r.lpop(cookie + 'repeatnum')
            commentnum = r.lpop(cookie + 'commentnum')

            res["time"]=(int(timeVal))
            res["likenum"]=(int(likenum))
            res["repeatnum"]=(int(repeatnum))
            res["commentnum"]=(int(commentnum))
        except:
            res={}
        return HttpResponse(json.dumps(res), content_type='application/json')

class sina1(View):
    def get(self,request):
        return  render(request,"singleweibo.html")
    def post(self,request):

        cookie = request.POST.get("cookie", "")
        url = request.POST.get("url", "")
        data = {"project": "sina", "spider": "sinaspider2", "cookie": cookie, "url": url}
        result = requests.post("http://120.78.196.125/schedule.json", data=data)
        result = json.loads(result.text)
        jobid = result["jobid"]
        return render(request, "result_sina1.html", {'cookie': cookie,'jobid':jobid})


class result1(View):
    def post(self,request):
        res={}
        r = redis.Redis(host='120.78.196.125', port=6379)
        try:
            cookie = request.POST.get("cookie","")
            timeVal=r.lpop(cookie+'datetime2')
            # name=r.lpop(cookie+'repeatname2').decode()
            res["time"] = int(timeVal.decode())
            # res["repeatname"]=name
        except:
            res={}
        return HttpResponse(json.dumps(res), content_type='application/json')

class sina2(View):

    def get(self,request):
        return  render(request,"fans.html")
    def post(self,request):
        cookie=request.POST.get("cookie","")
        url=request.POST.get("url","")
        data = {"project": "sina", "spider": "sinaspider3", "cookie": cookie, "url": url}
        result = requests.post("http://120.78.196.125/schedule.json", data=data)
        result = json.loads(result.text)
        jobid = result["jobid"]
        return render(request, "result_sina2.html", {'cookie': cookie,'jobid':jobid})


class result2(View):
    def post(self,request):
        res={}
        r = redis.Redis(host='120.78.196.125', port=6379)
        try:
            cookie = request.POST.get("cookie", "")
            location=r.lpop(cookie+'location3')
            if location:
                res["location"]=location.decode()
        except Exception as e:
            print(e)
            res = {}
        return HttpResponse(json.dumps(res), content_type='application/json')


class sina3(View):

    def get(self,request):
        return  render(request,"socialmap.html")
    def post(self,request):
        cookie = request.POST.get("cookie", "")
        url = request.POST.get("url", "")
        data = {"project": "sina", "spider": "sinaspider4", "cookie": cookie, "url": url}
        result = requests.post("http://120.78.196.125/schedule.json", data=data)
        result=json.loads(result.text)
        jobid=result["jobid"]
        return render(request, "result_sina3.html", {'cookie': cookie,'jobid':jobid})


class result3(View):
    def post(self,request):
        res = {}
        r = redis.Redis(host='120.78.196.125', port=6379)
        try:
            cookie = request.POST.get("cookie", "")
            fansparent = r.lpop(cookie + 'fansparent4')
            fansname=r.lpop(cookie + 'fansname4')
            fanslevel = r.lpop(cookie + 'fanslevel4')

            res["fansparent"]=fansparent.decode()
            res["fansname"]=fansname.decode()
            res["fanslevel"]=fanslevel.decode()
            print(res)
        except:
            res={}
        return HttpResponse(json.dumps(res), content_type='application/json')


class cancel(View):
    def post(self,request):
        res = {"code":"ok"}
        try:
            r = redis.Redis(host='120.78.196.125', port=6379)
            cookie = request.POST.get("cookie", "")
            jobid=request.POST.get("jobid","")
            data = {"project": "sina", "job": jobid}
            result = requests.post("http://120.78.196.125/cancel.json", data=data)
            result = requests.post("http://120.78.196.125/cancel.json", data=data)
            time.sleep(3)
            r.delete(*r.keys(("*" + cookie + "*")))
        except:
            res = {"code": "fail"}
        return HttpResponse(json.dumps(res), content_type='application/json')
