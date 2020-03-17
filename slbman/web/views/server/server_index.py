import json, time
from repository import models
from django.views import View
from utils.response import BaseResponse
from web.views.index import AuthRequire
from django.shortcuts import render, HttpResponse
from utils import dcm_add_modify_reset_user


class ServerIndexView(View):
    def get(self, request, *args, **kwargs):
        response = BaseResponse()
        username = request.session.get('user_name', None)
        user_obj = models.SlbUser.objects.filter(name=username).all().first()
        return render(request, 'server/server-index.html', {'response': response,  'user_obj': user_obj, 'username': username})


class ServerListView(View):
    def get(self, request, *args, **kwargs):
        server_obj = models.Ecs.objects.all()
        # disk_obj = models.EcsDisk.objects.filter(instance_id="i-bp10z2bfzxn7063ijsi3")
        # print("disk_obj: ", disk_obj)
        # for d in disk_obj:
        #     print(d.instance_id)
        # for s in server_obj:
        #     s.memory = s.memory / 1024
        #     try:
        #         disk_obj = models.EcsDisk.objects.filter(instance_id=s.instance_id)
        #         # if len(disk_obj) > 1:
        #         print("disk_obj: ", disk_obj.instance_id)
        #         # else:
        #         #     pass
        #     except Exception as e:
        #         print(str(e))

        return render(request, 'server/server-list.html', {'server_obj': server_obj})

#
# class CreateEcsView(View):
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
#             response.error = str(e)
#             return HttpResponse(json.dumps(response.error))
