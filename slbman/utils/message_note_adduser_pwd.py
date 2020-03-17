#!/usr/bin/env python
# coding=utf-8
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest


def user_random_pwd(chinese_name, name, tel_number, pwd):
    json_para = "{'name':'%s', 'username':'%s' ,'password':'%s'}" % (chinese_name, name, pwd)
    # json_para = "{'name':'%s','password':'%s'}" % (chinese_name, pwd)
    client = AcsClient('LTAI0kQj0a33u4I7', '5gfuk9MIsfP8JEzf8uOauN7OqVEIxj', 'cn-hangzhou')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', tel_number)
    request.add_query_param('SignName', "邻邻壹")
    request.add_query_param('TemplateCode', "SMS_175584661")
    request.add_query_param('TemplateParam', json_para)

    response = client.do_action_with_exception(request)
    # print(str(response, encoding='utf-8'))
    return response


if __name__ == '__main__':
    user_random_pwd('周军龙', 'zhoujunlong', '13501141316', '123456')
