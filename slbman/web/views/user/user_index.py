import json
import time
import requests
from utils import dingtalk
from utils import random_pwd
from repository import models
from django.views import View
from utils.response import BaseResponse
from web.views.index import AuthRequire
from django.shortcuts import render, HttpResponse
from utils import dcm_add_modify_reset_user
from utils import message_note_reset_pwd
from utils import message_note_adduser_pwd


def post_pwd(url, msg, callback=None):
    status = True
    try:
        response = requests.post(
            url=url,
            headers={},
            json=msg
        )
    except Exception as e:
        response = e
        status = False
    if callback:
        callback(status, response)
    res = response._content
    return res


def form_post(url, msg, callback=None):
    status = True
    head = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", 'Connection': 'close'}
    try:
        response = requests.post(
            url=url,
            headers=head,
            json=msg
        )
    except Exception as e:
        response = e
        status = False
    if callback:
        callback(status, response)
    res = response._content
    return res


def client_post_formurlencodeddata_requests(request_url, requestJSONdata):
    # 功能说明：发送以form表单数据格式（它要求数据名称（name）和数据值（value）之间以等号相连，与另一组name/value值之间用&相连。例如：parameter1=12345&parameter2=23456。）请求到远程服务器，并获取请求响应报文。该请求消息头要求为：{"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}。
    # 输入参数说明：接收请求的URL;请求报文数据，格式为name1=value1&name2=value2
    # 输出参数：请求响应报文
    requestJSONdata = str(requestJSONdata).replace("+", "%2B")
    requestdata = requestJSONdata.encode("utf-8")
    head = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", 'Connection': 'close'}


    # 客户端发送请求报文到服务端
    r = requests.post(request_url, data=requestdata, headers=head)

    # 客户端获取服务端的响应报文数据
    responsedata = r.text
    # print("get the status: ", r.status_code)

    # 返回请求响应报文
    return responsedata


class CDNIndexView(AuthRequire):
    def get(self, request, *args, **kwargs):
        username = request.session.get('user_name', None)
        return render(request, 'cdn/cdn-index.html', {'username': username})


class CDNRefreshView(AuthRequire):
    def get(self, request, *args, **kwargs):
        response = BaseResponse()

        # response.data = service_obj
        return render(request, 'cdn/cdn.html', {'response': response})


class UserIndexView(View):
    def get(self, request, *args, **kwargs):
        response = BaseResponse()
        username = request.session.get('user_name', None)
        user_obj = models.SlbUser.objects.filter(name=username).all().first()
        return render(request, 'user/user-index.html', {'user_obj': user_obj,  'username': username})


class UserListView(View):
    def get(self, request, *args, **kwargs):
        try:
            user_obj = models.DcUser.objects.all()
            for u in user_obj:
                u.vpn_stat = models.Vpn.objects.filter(user_name=u.user_name).values('vpn_stat')[0]['vpn_stat']
        except Exception as e:
            print('userListError: ', str(e))
        return render(request, 'user/user-list.html', {'user_obj': user_obj})


class UserEditView(View):
    def get(self, request, u_id):
        u_id = int(u_id)
        response = BaseResponse()
        u_obj = models.DcUser.objects.filter(id=u_id).all().first()
        return render(request, 'user/user-edit.html', {'response': response, 'user_obj': u_obj})


class UserEditPostView(View):

    def post(self, request):
        user_id = request.POST.get('user_id')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        overtime = request.POST.get('overtime')

        try:
            models.DcUser.objects.filter(id=user_id).update(email=email, tel=phone, tag=overtime)
            return HttpResponse(json.dumps('操作成功'))
        except Exception as e:
            res = json.loads(str(e))
            print('EditUserInfoError:', str(e))
            return HttpResponse(json.dumps(res.decode()))


class UserAddView(View):
    def get(self, request, *args, **kwargs):
        response = BaseResponse()
        return render(request, 'user/user-add.html', {'response': response})

    def post(self, request, *args, **kwargs):
        user_name = request.POST.get('user_name')
        display_name = request.POST.get('family_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        # user_pwd = request.POST.get('user_pwd')
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        user_pwd = random_pwd.random_str()  # 生成用户随机密码
        url = 'http://10.126.11.124:9000/user/add'
        msg = {'name': user_name,
               'displayname': display_name,
               'shortname': display_name,
               'givenname': display_name,
               'department': '苏州总部',
               'officename': '苏州办公区',
               'phone': phone,
               'email': email,
               'password': user_pwd}
        try:
            res = post_pwd(url, msg)
            res_status = res.decode()
            if '用户添加成功' in res_status:
                models.DcUser.objects.create(user_name=user_name, chinese_name=display_name, email=email,
                                             add_time=current_time, tel=phone, stats='1', tag='2099-12-31')
                models.Vpn.objects.create(user_name=user_name, vpn_stat=0)
                message_note_adduser_pwd.user_random_pwd(display_name, user_name, phone, user_pwd)  # 短信通知
        except Exception as e:
            res = json.loads(str(e))
            print('ModifyPwdError:', str(e))
        return HttpResponse(json.dumps(res.decode()))


class UserForbiddenView(View):
    def post(self, request, *args, **kwargs):
        user_name = request.POST.get('user_name')
        url = 'http://10.126.11.124:9000/user/disable'
        # msg = {'name': user_name}
        msg = 'name=%s' % user_name
        try:
            chinese_user_name_obj = models.DcUser.objects.filter(user_name=user_name).all().first()
            chinese_user_name = chinese_user_name_obj.chinese_name

            operation_username = request.session.get('user_name', None)
            operation_chinese_name_obj = models.SlbUser.objects.filter(name=operation_username).all().first()
            operation_chinese_name = operation_chinese_name_obj.tag

            # res = form_post(url, msg)
            res = client_post_formurlencodeddata_requests(url, msg)
            if '账户停用成功' in res:
                models.DcUser.objects.filter(user_name=user_name).update(stats='0')
                ding_msg = '''账户：%s 停用成功\n执行人：%s''' % (chinese_user_name, operation_chinese_name)
                dingtalk.send_message(ding_msg)
        except Exception as e:
            res = str(e)
        return HttpResponse(json.dumps(res))


class UserStartView(View):
    def post(self, request, *args, **kwargs):
        user_name = request.POST.get('user_name')
        url = 'http://10.126.11.124:9000/user/enable'
        # msg = {'name': user_name}
        msg = 'name=%s' % user_name
        try:
            chinese_user_name_obj = models.DcUser.objects.filter(user_name=user_name).all().first()
            chinese_user_name = chinese_user_name_obj.chinese_name

            operation_username = request.session.get('user_name', None)
            operation_chinese_name_obj = models.SlbUser.objects.filter(name=operation_username).all().first()
            operation_chinese_name = operation_chinese_name_obj.tag

            # res = form_post(url, msg)
            res = client_post_formurlencodeddata_requests(url, msg)
            if '账户启用成功' in res:
                models.DcUser.objects.filter(user_name=user_name).update(stats='1')
                
                ding_msg = '''账户：%s 启用成功\n执行人：%s''' % (chinese_user_name, operation_chinese_name)
                dingtalk.send_message(ding_msg)
        except Exception as e:
            res = str(e)
        return HttpResponse(json.dumps(res))


class ResetPwdView(View):
    def post(self, request, *args, **kwargs):
        u_name = request.POST.get('user_name')
        user_obj = models.DcUser.objects.filter(user_name=u_name).values('chinese_name', 'tel')
        u_chinese_name = user_obj[0]['chinese_name']
        u_tel = user_obj[0]['tel']
        new_pwd = random_pwd.random_str()  # 生成用户随机密码
        url = 'http://10.126.11.124:9000/user/reset_password'
        msg = {'Name': u_name, 'Newpwd': new_pwd}
        try:
            chinese_user_name_obj = models.DcUser.objects.filter(user_name=u_name).all().first()
            chinese_user_name = chinese_user_name_obj.chinese_name

            operation_username = request.session.get('user_name', None)
            operation_chinese_name_obj = models.SlbUser.objects.filter(name=operation_username).all().first()
            operation_chinese_name = operation_chinese_name_obj.tag

            res = post_pwd(url, msg)
            if '密码重置成功' in res.decode():
                message_note_reset_pwd.reset_pwd(u_tel, u_chinese_name, new_pwd)
                
                ding_msg = '''账户：%s 密码重置成功\n执行人：%s''' % (chinese_user_name, operation_chinese_name)
                dingtalk.send_message(ding_msg)
        except Exception as e:
            res = str(e)
            print('ResetPwdError:', e)
        return HttpResponse(json.dumps(res.decode()))


###新版调用研发接口添加用户方法
# class UserAddView(View):
#     def get(self, request, *args, **kwargs):
#         response = BaseResponse()
#         return render(request, 'user/user-add.html', {'response': response})
#
#     def post(self, request, *args, **kwargs):
#         response = BaseResponse()
#         try:
#             operation = request.POST.get('operation')
#             username = request.POST.get('username')
#             family_name = request.POST.get('family_name')
#             given_name = request.POST.get('given_name')
#             tel = request.POST.get('tel')
#             email = request.POST.get('email')
#             working_place = request.POST.get('working_place')
#             pwd = request.POST.get('pwd')
#             display_name = family_name + given_name
#             # current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#             current_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
#             if operation == 'add_user':
#                 if username:
#                     slb_obj = models.DcmUser.objects.filter(user_name=username).all().first()
#                     if slb_obj:
#                         response.data = '用户已存在,不能重复添加!'
#                     else:
#                         # 这里需要调用添加用户api返回添加用户成功后再在数据库中插入该用户信息
#                         # add_user_res = dcm_add_modify_reset_user.add_user(username, display_name, tel, email, pwd)
#                         add_user_res = '添加用户成功'
#                         if add_user_res == '添加用户成功':
#                             models.DcmUser.objects.create(user_name=username, family_name=family_name,
#                                                           given_name=given_name, tel_number=tel, email=email,
#                                                           working_place=working_place, vpn=0, password=pwd, tag=0,
#                                                           add_time=current_time)
#                         # 这里需要调用雨馨接口同步用户信息
#                 else:
#                     response.data = 'Error:系统异常(EcsUpDownView)'
#             elif operation == 'modify_user':
#                 if username:
#                     slb_obj = models.DcmUser.objects.filter(username=username).all().first()
#                     if slb_obj:
#                         modify_user_res = dcm_add_modify_reset_user.modify_user()
#                     else:
#                         response.data = '用户不存在!'
#             return HttpResponse(json.dumps(response.data))
#         except Exception as e:
#             raise str(e)
#             response.error = str(e)
#             return HttpResponse(json.dumps(response.error))
