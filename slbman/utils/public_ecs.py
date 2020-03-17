#!/usr/bin/env python
# coding=utf-8
import json
import sqlite3
import sys
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

conn = sqlite3.connect("aliyun.db")
cursor = conn.cursor()
# cursor.execute("create table slb_vid (id varchar(32) primary key, name varchar(64))")
client = AcsClient('LTAIpndTajSPl2rB', 'SI6cezZyifWS6qbmvWAOGnxi3ktWa0', 'cn-hangzhou')


def getecsip(ecsid):
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('ecs.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2014-05-26')
    request.set_action_name('DescribeInstances')
    request.add_query_param('RegionId', 'cn-hangzhou')
    request.add_query_param('InstanceIds', "['"+ecsid+"']")
    response = client.do_action(request)
    jsonData = json.loads(response)
    return jsonData['Instances']['Instance'][0]['NetworkInterfaces']['NetworkInterface'][0]['PrimaryIpAddress']


def getvgattr(vgid):
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('slb.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2014-05-15')
    request.set_action_name('DescribeVServerGroupAttribute')
    request.add_query_param('RegionId', 'cn-hangzhou')
    request.add_query_param('VServerGroupId', vgid)
    response = client.do_action(request)
    jsonData = json.loads(response)
    #for vgattr in jsonData['BackendServers']['BackendServer']:
        #print("%s实例ID:%s\t权重:%d\tIP地址:%s\t端口:%d" % (
            #vgattr['Type'], vgattr['ServerId'], vgattr['Weight'], getecsip(vgattr['ServerId']), vgattr['Port']))
        #print(type(vgattr['ServerId']), type(vgattr['Weight']), type(getecsip(vgattr['ServerId'])),  type(vgattr['Port']))


def checkstatus(action,response, ecsid):
    jsonData = json.loads(response)
    for vgattr in jsonData['BackendServers']['BackendServer']:
        if vgattr['ServerId'] == ecsid:
            if action == 'up':
                return True
        else:
            if action == 'down':
                return True
    return False


def getslblist():
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('slb.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2014-05-15')
    request.set_action_name('DescribeVServerGroups')
    request.add_query_param('RegionId', 'cn-hangzhou')
    request.add_query_param('LoadBalancerId', 'lb-bp198gpxhi1jtoh7htcbv')
    response = client.do_action(request)
    jsonData = json.loads(response)
    for vserver in jsonData['VServerGroups']['VServerGroup']:
        # print("负载实例ID:" + vserver['VServerGroupId'])
        # print("负载实例名称:" + vserver['VServerGroupName'])
        getvgattr(vserver['VServerGroupId'])
        # cursor.execute('insert into slb_vid (id, name) values (\'%s\', \'%s\')'%(vserver['VServerGroupId'],vserver['VServerGroupName']))
        # conn.commit()
        conn.close()


def disable(vgid, ecsid, port, weight):
    backends = "[{'ServerId':'%s','Port':'%d','Weight':'%d'}]" % (ecsid, port, weight)
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('slb.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2014-05-15')
    request.set_action_name('RemoveVServerGroupBackendServers')
    request.add_query_param('RegionId', 'cn-hangzhou')
    request.add_query_param('VServerGroupId', vgid)
    request.add_query_param('BackendServers', backends)
    response = client.do_action_with_exception(request)
    if checkstatus('down', response, ecsid):
        return "下负载成功"
    else:
        return "下负载失败"


def enable(vgid,ecsid,port,weight):
    backends = "[{'ServerId':'%s','Port':'%d','Weight':'%d'}]" % (ecsid, port, weight)
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('slb.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2014-05-15')
    request.set_action_name('AddVServerGroupBackendServers')
    request.add_query_param('RegionId', 'cn-hangzhou')
    request.add_query_param('VServerGroupId', vgid)
    request.add_query_param('BackendServers', backends)
    response = client.do_action_with_exception(request)
    if checkstatus('up', response, ecsid):
        return "上负载成功"
    else:
        return "上负载失败"


def main(argv):
    print(argv)
    #disable("rsp-bp1wynm6mzkg6","i-bp1gnntqxw2xkeaqbnpa",2181,100)
    getslblist()
    # enable("rsp-bp1wynm6mzkg6","i-bp1gnntqxw2xkeaqbnpa",2181,100)
    #getslblist()
    return


if __name__ == '__main__':
    main(sys.argv)
