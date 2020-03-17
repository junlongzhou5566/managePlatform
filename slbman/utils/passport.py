import requests
from urllib import parse
from django.views import View
from repository import models
from utils.response import BaseResponse
from ldap3 import Connection, ServerPool
from django.shortcuts import render, HttpResponse


class PassportAPI(View):
    def post(self, request, *args, **kwargs):
        '''
        接收ajax数据实现用户验证
        :param request:
        :param args:
        :param kwargs:
        :return: response.data
        '''
        response = BaseResponse()

        username = request.POST.get('username')
        pwd = request.POST.get('pwd').strip()
        pwd2 = parse.quote(pwd)
        usr_obj = models.SlbUser.objects.filter(name=username).all().first()
        if not usr_obj:
            response.data = '{"code":"没有权限"}'
            return HttpResponse(response.data)
        else:
            try:
                ldap_server_pool = ServerPool(["10.126.10.4", "10.126.11.150"])
                conn = Connection(ldap_server_pool, user=username+'@lly.com', password=pwd,
                                  check_names=True, lazy=False, raise_exceptions=False)
                conn.open()
                conn.bind()
                print(conn.result)
                if username is not None and conn.result["description"] == "success":
                    request.session['user_name'] = username
                    response.data = '{"code": "200"}'
                else:
                    response.data = '{"code": "认证失败"}'
            except Exception as e:
                response.data = str(e)
                pass
        return HttpResponse(response.data)
