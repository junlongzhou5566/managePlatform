import json
from utils import dingtalk
from repository import models
from django.views import View
from django.shortcuts import  HttpResponse


class StartVpn(View):

    def post(self, request, *args, **kwargs):
        user_name = request.POST.get('user_name')
        try:
            chinese_user_name_obj = models.DcUser.objects.filter(user_name=user_name).all().first()
            chinese_user_name = chinese_user_name_obj.chinese_name

            operation_username = request.session.get('user_name', None)
            operation_chinese_name_obj = models.SlbUser.objects.filter(name=operation_username).all().first()
            operation_chinese_name = operation_chinese_name_obj.tag

            models.Vpn.objects.filter(user_name=user_name).update(vpn_stat=1)

            ding_msg = '''账户：%s vpn 启用成功\n执行人：%s''' % (chinese_user_name, operation_chinese_name)
            dingtalk.send_message(ding_msg)

            res = '执行成功！！！'
        except Exception as e:
            res = str(e)
        return HttpResponse(json.dumps(res))


class ForbiddenVpn(View):

    def post(self, request, *args, **kwargs):
        user_name = request.POST.get('user_name')
        try:
            chinese_user_name_obj = models.DcUser.objects.filter(user_name=user_name).all().first()
            chinese_user_name = chinese_user_name_obj.chinese_name

            operation_username = request.session.get('user_name', None)
            operation_chinese_name_obj = models.SlbUser.objects.filter(name=operation_username).all().first()
            operation_chinese_name = operation_chinese_name_obj.tag

            models.Vpn.objects.filter(user_name=user_name).update(vpn_stat=0)

            ding_msg = '''账户：%s vpn 禁用成功\n执行人：%s''' % (chinese_user_name, operation_chinese_name)
            dingtalk.send_message(ding_msg)
            res = '执行成功！！！'
        except Exception as e:
            res = str(e)
        return HttpResponse(json.dumps(res))
