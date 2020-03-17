import os, json, time
import requests
from repository import models
from urllib import parse
from repository import models
from django.views import View
from utils.response import BaseResponse
from web.views.index import AuthRequire
from django.shortcuts import render, HttpResponse, redirect


####"https://cdn.api.baishan.com/v2/cache/refresh?token=xxx"####
cdn_url = 'https://cdn.api.baishan.com/v2/cache/refresh'
cdn_token = '8be82ef92f5b8b18670903898a69eaa0'
url_token = cdn_url + '?token=' + cdn_token


def curl_post(url, msg):
    cmd = 'curl -X POST "'+url+'" -H "Content-Type: application/json" -d ' + msg
    res = os.popen(cmd).readlines()
    return res


class CDNIndexView(AuthRequire):

    def get(self, request, *args, **kwargs):
        response = BaseResponse
        username = request.session.get('user_name', None)
        record_obj = models.CdnFreshRecord.objects.all().order_by('-fresh_time')
        response.data = record_obj
        user_obj = models.SlbUser.objects.filter(name=username).all().first()
        return render(request, 'cdn/cdn-index.html', {'username': username, 'user_obj': user_obj, 'record_obj': record_obj})


class CDNRefreshView(AuthRequire):

    def get(self, request, *args, **kwargs):
        return render(request, 'cdn/cdn.html')

    def post(self, request, *args, **kwargs):
        response = BaseResponse()
        url_str = ''
        fresh_type_ = ''
        fresh_type = request.POST.get('fresh_type')
        fresh_content = request.POST.get('fresh_content')
        fresh_content_list = fresh_content.split('\n')
        for u in fresh_content_list:
            url_str = url_str + '"' + u + '"'
            url_str = url_str.replace('""', '","')
        if fresh_type == '目录':
            fresh_type = 'dir'
        msg = '{"urls":[' + url_str + '],"type":"' + fresh_type + '"}'
        msg = json.dumps(msg)
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        try:
            cdn_res = curl_post(url_token, msg)
            print(cdn_res)
            if '{"code":0,' in cdn_res[0]:
                response.data = '执行成功！'
                if fresh_type == 'url':
                    fresh_type_ = 'URL刷新'
                elif fresh_type == '目录':
                    fresh_type_ = '目录刷新'
                for u in fresh_content_list:
                    models.CdnFreshRecord.objects.create(fresh_content=u, fresh_type=fresh_type_,
                                                         fresh_time=current_time, stats='完成')
        except Exception as e:
            response.data = str(e)
        return HttpResponse(json.dumps(response.data))
