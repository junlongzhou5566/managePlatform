#!/usr/bin/env python
# coding=utf-8
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest


def reset_pwd(u_tel, user_chinese_name, new_pwd):
    json_para = "{'name':'%s','password':'%s'}" % (user_chinese_name, new_pwd)
    client = AcsClient('LTAI0kQj0a33u4I7', '5gfuk9MIsfP8JEzf8uOauN7OqVEIxj', 'cn-hangzhou')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', u_tel)
    request.add_query_param('SignName', "邻邻壹")
    request.add_query_param('TemplateCode', "SMS_175584659")
    request.add_query_param('TemplateParam', json_para)

    response = client.do_action_with_exception(request)
    # print(str(response, encoding='utf-8'))
    return response


if __name__ == '__main__':
    reset_pwd('13501141316', '周军龙', 'zhoujunlong')
