#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
client = AcsClient('<accessKeyId>', '<accessSecret>', 'cn-hangzhou')

request = CommonRequest()
request.set_accept_format('json')
request.set_domain('dysmsapi.aliyuncs.com')
request.set_method('POST')
request.set_protocol_type('https') # https | http
request.set_version('2017-05-25')
request.set_action_name('SendSms')

request.add_query_param('RegionId', "cn-hangzhou")
request.add_query_param('PhoneNumbers', "13811782191")
request.add_query_param('SignName', "邻邻壹")
request.add_query_param('TemplateCode', "SMS_12312312")
request.add_query_param('TemplateParam', "{'name':'yanyan','username':'yanyan','password':'123456'}")

response = client.do_action(request)
print(str(response, encoding='utf-8'))
