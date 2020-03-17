import json
from urllib import parse
from repository import models
from django.views import View
from utils.response import BaseResponse
from ldap3 import Connection, ServerPool
from utils import ecs, public_ecs, dingtalk, ecs_direct
from django.shortcuts import render, HttpResponse, redirect


class AuthRequire(View):
    '''
    验证用户时候登录，没有登录则跳转至登录页面
    '''
    def dispatch(self, request, *args, **kwargs):
        try:
            user = request.session.get('user_name', None)
            if not user:
                return redirect("/login")
        except Exception as e:
            print(str(e))
            pass
        return super(AuthRequire, self).dispatch(request, *args, **kwargs)


class TestView(AuthRequire):
    def get(self, request, *args, **kwargs):
        return render(request, 'ecs/test.html')


class FsTestView(AuthRequire):
    def get(self, request, *args, **kwargs):
        return render(request, 'test/fs_test.html')


class IndexView(AuthRequire):
    def get(self, request, *args, **kwargs):
        username = request.session.get('user_name', None)
        user_obj = models.SlbUser.objects.filter(name=username).all().first()
        return render(request, 'index/index.html', {'user_obj': user_obj, 'username': username})


class LogoView(AuthRequire):
    def get(self, request, *args, **kwargs):
        response = BaseResponse()
        user = request.session.get('user_name')
        user_obj = models.SlbUser.objects.filter(name=user).all().first()
        return render(request, 'index/logo.html', {'response': response, 'user_obj': user_obj, 'username': user})



class PrivateView(AuthRequire):
    def get(self, request, *args, **kwargs):
        username = request.session.get('user_name', None)
        user_obj = models.SlbUser.objects.filter(name=username).all().first()
        return render(request, 'private.html', {'user_obj': user_obj, 'username': username})


class WelcomeView(AuthRequire):
    def get(self, request, *args, **kwargs):
        slb_list = ['lb-bp14c9cltijb7fhq31bd4', 'lb-bp111xg3j67beh4ow6l2o']
        response = BaseResponse()
        service = request.session.get('service')

        user = request.session.get('user_name')
        user_obj = models.SlbUser.objects.filter(name=user).all().first()
        if user_obj.group == '1':
            project_obj = models.ServiceToSlb.objects.filter(slb_id__in=slb_list).all()
        else:
            project_obj = models.ServiceToSlb.objects.filter(slb_id__in=slb_list, group=user_obj.group).all()
        if service == '全 部':
            service_obj = models.SlbInfo.objects.all()
        else:
            slb_obj = models.ServiceToSlb.objects.filter(service_name=service, slb_id__in=slb_list).all().first()
            if slb_obj:
                service_obj = models.SlbInfo.objects.filter(vg_id=slb_obj.vg_id).all()
                for s in service_obj:
                    s_id = s.vg_id
                    tag_obj = models.ServiceToSlb.objects.filter(vg_id=s_id).all().first()
                    if tag_obj:
                        tag = tag_obj.tag
                        s_name = tag_obj.service_name
                    else:
                        tag = ''
                        s_name = ''
                        print('error:', s_id)
                    s.tag = tag
                    s.s_name = s_name
            else:
                service_obj = models.SlbInfo.objects.all()
                for s in service_obj:
                    s_id = s.vg_id
                    tag_obj = models.ServiceToSlb.objects.filter(vg_id=s_id).all().first()
                    if tag_obj:
                        tag = tag_obj.tag
                        s_name = tag_obj.service_name
                    else:
                        tag = ''
                        s_name = ''
                        print('error:', s_id)
                    s.tag = tag
                    s.s_name = s_name
        response.data = service_obj
        return render(request, 'welcome.html', {'response': response, 'service': service, 'project_obj': project_obj,
                                                'user_obj': user_obj, 'username': user})


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        try:
            del request.session['user_name']
        except KeyError:
            pass
        return redirect('/login')


class PublicView(AuthRequire):
    def get(self, request, *args, **kwargs):
        username = request.session.get('user_name', None)
        user_obj = models.SlbUser.objects.filter(name=username).all().first()
        return render(request, 'index2.html', {'user_obj': user_obj, 'username': username})


class PublicSlbView(AuthRequire):
    def get(self, request, *args, **kwargs):
        response = BaseResponse()
        service = request.session.get('service')
        slb_id = ['lb-bp198gpxhi1jtoh7htcbv', 'lb-bp1rbidt0xozztl0ap7pz']
        user = request.session.get('user_name')
        usr_obj = models.SlbUser.objects.filter(name=user).all().first()
        if usr_obj.group == '1':
            project_obj = models.ServiceToSlb.objects.filter(slb_id__in=slb_id).all()
        else:
            project_obj = models.ServiceToSlb.objects.filter(slb_id__in=slb_id, group=usr_obj.group).all()
        if service == '全 部':
            service_obj = models.SlbInfo.objects.all()
        else:
            slb_obj = models.ServiceToSlb.objects.filter(service_name=service, slb_id__in=slb_id).all().first()
            if slb_obj:
                service_obj = models.SlbInfo.objects.filter(vg_id=slb_obj.vg_id, slb_id__in=slb_id).all()
                for s in service_obj:
                    s_id = s.vg_id
                    tag_obj = models.ServiceToSlb.objects.filter(vg_id=s_id).all().first()
                    if tag_obj:
                        tag = tag_obj.tag
                        s_name = tag_obj.service_name
                    else:
                        tag = ''
                        s_name = ''
                        print('error:', s_id)
                    s.tag = tag
                    s.s_name = s_name
            else:
                service_obj = models.SlbInfo.objects.all()
                for s in service_obj:
                    s_id = s.vg_id
                    tag_obj = models.ServiceToSlb.objects.filter(vg_id=s_id).all().first()
                    if tag_obj:
                        tag = tag_obj.tag
                        s_name = tag_obj.service_name
                    else:
                        tag = ''
                        s_name = ''
                        print('error:', s_id)
                    s.tag = tag
                    s.s_name = s_name
        response.data = service_obj
        return render(request, 'public.html', {'response': response, 'service': service, 'project_obj': project_obj})


class HostView(View):
    def post(self, request, *args, **kwargs):
        '''
        接收ajax数据，根据项目筛选容器信息
        :param request:
        :param args:
        :param kwargs:
        :return: response.data
        '''
        response = BaseResponse()
        try:
            service = request.POST.get('service')
            if service:
                service = service.strip()
                request.session['service'] = service
            response.data = 'OK'
            return HttpResponse(json.dumps(response.data))
        except Exception as e:
            response.error = e
            return HttpResponse(json.dumps(response.error))


class EcsUpDownView(View):
    def post(self, request, *args, **kwargs):
        response = BaseResponse()
        try:
            ip = request.POST.get('ip')
            operation = request.POST.get('operation')
            username = request.session.get('user_name', None)
            chinese_name_obj = models.SlbUser.objects.filter(name=username).all().first()
            chinese_name = chinese_name_obj.tag
            if ip:
                slb_obj = models.SlbInfo.objects.filter(ecs_ip=ip.strip(), slb_id='lb-bp14c9cltijb7fhq31bd4').all().first()
                if slb_obj:
                    vg_id = slb_obj.vg_id
                    ecs_id = slb_obj.ecs_id
                    port = slb_obj.port
                    weight = slb_obj.weight
                    if operation.strip() == '下线':
                        response.data = ecs.disable(vg_id, ecs_id, port, weight)
                        service_name_obj = models.ServiceToSlb.objects.filter(vg_id=vg_id, slb_id='lb-bp14c9cltijb7fhq31bd4').all().first()
                        if response.data == '下负载成功':
                            response.data = ip + ': ' + response.data
                            msg = '''负载名称：LLY-内部生产系统-内网\n实例IP：%s\n服务名称：%s\n执行人：%s\n下负载操作已完成!''' % (ip, service_name_obj.service_name, chinese_name)
                            dingtalk.send_message(msg)
                            models.SlbInfo.objects.filter(ecs_ip=ip, slb_id='lb-bp14c9cltijb7fhq31bd4').update(stats='0')
                    elif operation.strip() == '上线':
                        response.data = ecs.enable(vg_id, ecs_id, port, weight)
                        service_name_obj = models.ServiceToSlb.objects.filter(vg_id=vg_id, slb_id='lb-bp14c9cltijb7fhq31bd4').all().first()
                        if response.data == '上负载成功':
                            response.data = ip + ': ' + response.data
                            msg = '''负载名称：LLY-内部生产系统-内网\n实例IP：%s\n服务名称：%s\n执行人：%s\n上负载操作已完成!''' % (ip, service_name_obj.service_name, chinese_name)
                            dingtalk.send_message(msg)
                            models.SlbInfo.objects.filter(ecs_ip=ip, slb_id='lb-bp14c9cltijb7fhq31bd4').update(stats='1')
                else:
                    new_slb_id = 'lb-bp111xg3j67beh4ow6l2o'
                    slb_obj = models.SlbInfo.objects.filter(ecs_ip=ip.strip(),slb_id=new_slb_id).all().first()
                    if slb_obj:
                        vg_id = slb_obj.vg_id
                        ecs_id = slb_obj.ecs_id
                        port = slb_obj.port
                        weight = slb_obj.weight
                        if operation.strip() == '下线':
                            response.data = ecs.disable(vg_id, ecs_id, port, weight)
                            service_name_obj = models.ServiceToSlb.objects.filter(vg_id=vg_id, slb_id=new_slb_id).all().first()
                            if response.data == '下负载成功':
                                response.data = ip + ': ' + response.data
                                msg = '''负载名称：LLY生产-内网负载-02\n实例IP：%s\n服务名称：%s\n执行人：%s\n下负载操作已完成!''' % (ip, service_name_obj.service_name, chinese_name)
                                dingtalk.send_message(msg)
                                models.SlbInfo.objects.filter(ecs_ip=ip, slb_id=new_slb_id).update(stats='0')
                        elif operation.strip() == '上线':
                            response.data = ecs.enable(vg_id, ecs_id, port, weight)
                            service_name_obj = models.ServiceToSlb.objects.filter(vg_id=vg_id, slb_id=new_slb_id).all().first()
                            if response.data == '上负载成功':
                                response.data = ip + ': ' + response.data
                                msg = '''负载名称：LLY生产-内网负载-02\n实例IP：%s\n服务名称：%s\n执行人：%s\n上负载操作已完成!''' % (ip, service_name_obj.service_name, chinese_name)
                                dingtalk.send_message(msg)
                                models.SlbInfo.objects.filter(ecs_ip=ip, slb_id=new_slb_id).update(stats='1')
                    else:
                        response.data = 'Error:未匹配到服务器信息!'
            else:
                response.data = 'Error:系统异常(EcsUpDownView)'
                # else:
                #     response.data = '未匹配到服务器信息!'
            return HttpResponse(json.dumps(response.data))
        except Exception as e:
            response.error = str(e)
            return HttpResponse(json.dumps(response.error))


class PublicSlbEcsUpDownView(View):
    def post(self, request, *args, **kwargs):
        response = BaseResponse()
        slb_id = ['lb-bp198gpxhi1jtoh7htcbv', 'lb-bp1rbidt0xozztl0ap7pz']
        try:
            ip = request.POST.get('ip')
            operation = request.POST.get('operation')
            username = request.session.get('user_name', None)
            chinese_name_obj = models.SlbUser.objects.filter(name=username).all().first()
            chinese_name = chinese_name_obj.tag
            if ip:
                slb_obj = models.SlbInfo.objects.filter(ecs_ip=ip.strip(), slb_id='lb-bp198gpxhi1jtoh7htcbv').all().first()
                if slb_obj:
                    vg_id = slb_obj.vg_id
                    ecs_id = slb_obj.ecs_id
                    port = slb_obj.port
                    weight = slb_obj.weight
                    if operation.strip() == '下线':
                        response.data = public_ecs.disable(vg_id, ecs_id, port, weight)
                        service_name_obj = models.ServiceToSlb.objects.filter(vg_id=slb_obj.vg_id).all().first()
                        if response.data == '下负载成功':
                            response.data = ip + ': ' + response.data
                            msg = '''负载名称：LLY-内部生产系统-外网\n实例IP：%s\n服务名称：%s\n执行人：%s\n下负载操作已完成!''' % (ip, service_name_obj.service_name, chinese_name)
                            dingtalk.send_message(msg)
                            models.SlbInfo.objects.filter(ecs_ip=ip, slb_id='lb-bp198gpxhi1jtoh7htcbv').update(stats='0')
                    elif operation.strip() == '上线':
                        response.data = public_ecs.enable(vg_id, ecs_id, port, weight)
                        service_name_obj = models.ServiceToSlb.objects.filter(vg_id=slb_obj.vg_id).all().first()
                        if response.data == '上负载成功':
                            response.data = ip + ': ' + response.data
                            msg = '''负载名称：LLY-内部生产系统-外网\n实例IP：%s\n服务名称：%s\n执行人：%s\n上负载操作已完成!''' % (ip, service_name_obj.service_name, chinese_name)
                            dingtalk.send_message(msg)
                            models.SlbInfo.objects.filter(ecs_ip=ip, slb_id='lb-bp198gpxhi1jtoh7htcbv').update(stats='1')
                else:
                    front_public_slb_id='lb-bp1rbidt0xozztl0ap7pz'
                    slb_obj = models.SlbInfo.objects.filter(ecs_ip=ip.strip(),
                                                            slb_id=front_public_slb_id).all().first()
                    if slb_obj:

                        # vg_id = slb_obj.vg_id
                        ecs_id = slb_obj.ecs_id
                        port = slb_obj.port
                        weight = slb_obj.weight
                        if operation.strip() == '下线':
                            response.data = ecs_direct.disable(front_public_slb_id, ecs_id, port, weight)
                            service_name_obj = models.ServiceToSlb.objects.filter(vg_id=slb_obj.vg_id).all().first()
                            if response.data == '下负载成功':
                                response.data = ip + ': ' + response.data
                                msg = '''负载名称：LLY-内部生产系统-外网\n实例IP：%s\n服务名称：%s\n执行人：%s\n下负载操作已完成!''' % (ip, service_name_obj.service_name, chinese_name)
                                dingtalk.send_message(msg)
                                models.SlbInfo.objects.filter(ecs_ip=ip, slb_id=front_public_slb_id).update(stats='0')
                        elif operation.strip() == '上线':
                            response.data = ecs_direct.enable(front_public_slb_id, ecs_id, port, weight)
                            service_name_obj = models.ServiceToSlb.objects.filter(vg_id=slb_obj.vg_id).all().first()
                            if response.data == '上负载成功':
                                response.data = ip + ': ' + response.data
                                msg = '''负载名称：LLY-内部生产系统-外网\n实例IP：%s\n服务名称：%s\n执行人：%s\n上负载操作已完成!''' % (ip, service_name_obj.service_name, chinese_name)
                                dingtalk.send_message(msg)
                                models.SlbInfo.objects.filter(ecs_ip=ip, slb_id=front_public_slb_id).update(stats='1')
                    else:
                        response.data = 'Error:未匹配到服务器信息!'
            else:
                response.data = 'Error:系统异常(PublicSlbEcsUpDownView)'
            return HttpResponse(json.dumps(response.data))
        except Exception as e:
            response.error = str(e)
            return HttpResponse(json.dumps(response.error))


class MemberListView(View):
    def get(self, request, *args, **kwargs):
        response = BaseResponse()
        service = request.session.get('service')
        project_obj = models.ServiceToSlb.objects.all()
        if service == '全 部':
            service_obj = models.SlbInfo.objects.all()
        else:
            slb_obj = models.ServiceToSlb.objects.filter(service_name=service).all().first()
            if slb_obj:
                service_obj = models.SlbInfo.objects.filter(vg_id=slb_obj.vg_id).all()
                for s in service_obj:
                    s_id = s.vg_id
                    tag_obj = models.ServiceToSlb.objects.filter(vg_id=s_id).all().first()
                    if tag_obj:
                        tag = tag_obj.tag
                        s_name = tag_obj.service_name
                    else:
                        tag = ''
                        s_name = ''
                        print('error:', s_id)
                    s.tag = tag
                    s.s_name = s_name
            else:
                service_obj = models.SlbInfo.objects.all()
                for s in service_obj:
                    s_id = s.vg_id
                    tag_obj = models.ServiceToSlb.objects.filter(vg_id=s_id).all().first()
                    if tag_obj:
                        tag = tag_obj.tag
                        s_name = tag_obj.service_name
                    else:
                        tag = ''
                        s_name = ''
                        print('error:', s_id)
                    s.tag = tag
                    s.s_name = s_name
        response.data = service_obj
        return render(request, 'member-list.html', {'response': response, 'service': service, 'project_obj': project_obj})


# class HistoryDataView(View):
#     def get(self, request, *args, **kwargs):
#         try:
#             list_obj = []
#             tmp_dict = {}
#             res_dict = {('1:00', '1'), ('2:00', '2'), ('3:00', '3'), ('4:00', '4'), ('5:00', '5')}
#             for i in res_dict:
#                 tmp_dict['clock'] = i[0]
#                 tmp_dict['value'] = i[1]
#                 list_obj.insert(0, json.dumps(tmp_dict))
#         except Exception as e:
#             print(str(e))
#             list_obj = []
#         return HttpResponse(json.dumps(list_obj))
