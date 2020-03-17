#!/usr/bin/env python
# coding=utf-8
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcdn.request.v20180510.RefreshObjectCachesRequest import RefreshObjectCachesRequest


client = AcsClient('LTAIpndTajSPl2rB', 'SI6cezZyifWS6qbmvWAOGnxi3ktWa0', 'cn-hangzhou')


def refresh_cache(path, fresh_type):
    request = RefreshObjectCachesRequest()
    request.set_accept_format('json')

    request.set_ObjectPath(path)  # 刷新单个url
    request.set_ObjectType(fresh_type)
    # request.set_ObjectPath("http://lly-img.linlinyi.cn/wxapp/1.1.0/ling/bg_redpacket_new1x.png")  # 刷新单个url
    # request.set_ObjectType("URL")

    response = client.do_action_with_exception(request)
    print(str(response, encoding='utf-8'))


def main():
    refresh_cache("http://lly-img.linlinyi.cn/wxapp/1.1.0/ling/bg_redpacket_new1x.png", "URL")
    return


if __name__ == '__main__':
    main()
