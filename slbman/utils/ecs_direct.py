#!/usr/bin/env python
# coding=utf-8
import json
import sqlite3
import sys
from aliyunsdkcore.request import CommonRequest
from aliyunsdkcore.client import AcsClient


conn = sqlite3.connect("aliyun.db")
cursor = conn.cursor()
client = AcsClient('LTAIpndTajSPl2rB', 'SI6cezZyifWS6qbmvWAOGnxi3ktWa0', 'cn-hangzhou')


def checkstatus(action, response, ecsid):
    jsonData = json.loads(response)
    for vgattr in jsonData['BackendServers']['BackendServer']:
        if vgattr['ServerId'] == ecsid:
            if action == 'up':
                return True
        else:
            if action == 'down':
                return True
    return False


def disable(slbid, ecsid, port, weight):
    backends = "[{'ServerId':'%s','Port':'%d','Weight':'%d'}]" % (ecsid, port, weight)
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('slb.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2014-05-15')
    request.set_action_name('RemoveBackendServers')
    request.add_query_param('RegionId', 'cn-hangzhou')
    request.add_query_param('LoadBalancerId', slbid)
    request.add_query_param('BackendServers', backends)
    response = client.do_action_with_exception(request)
    if checkstatus('down', response, ecsid):
        return "下负载成功"
    else:
        return "下负载失败"


def enable(slbid, ecsid, port, weight):
    backends = "[{'ServerId':'%s','Port':'%d','Weight':'%d'}]" % (ecsid, port, weight)
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('slb.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2014-05-15')
    request.set_action_name('AddBackendServers')
    request.add_query_param('RegionId', 'cn-hangzhou')
    request.add_query_param('LoadBalancerId', slbid)
    request.add_query_param('BackendServers', backends)
    response = client.do_action_with_exception(request)
    if checkstatus('up', response, ecsid):
        return "上负载成功"
    else:
        return "上负载失败"


def main(argv):
    #disable("lb-bp1rbidt0xozztl0ap7pz", "i-bp15oiwjv3fwk3pmnnmp", 8080, 100)
    #enable("lb-bp1rbidt0xozztl0ap7pz", "i-bp15oiwjv3fwk3pmnnmp", 8080, 100)
    return


if __name__ == '__main__':
    main(sys.argv)
