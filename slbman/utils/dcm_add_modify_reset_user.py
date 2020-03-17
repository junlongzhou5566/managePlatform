#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import requests
from django.views import View
from django.shortcuts import render, HttpResponse


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


def add_user(name, displayname, phone,email, password):
    url = 'http://10.126.11.124:9000/user/add'
    print(url)
    msg = {'name': name, 'displayname': displayname, 'phone': phone, 'email': email, 'password': password}
    try:
        res = post_pwd(url, msg)
        print(res)
    except Exception as e:
        print(str(e))
        # raise str(e)
        res = json.loads(str(e))
        print('AddUserError:', e)
    return json.dumps(res.decode())


def modify_user(name, old_pwd, new_pwd):
    url = 'http://10.126.11.124:9000/user/modify_password'
    msg = {'Name': name, 'Oldpwd': old_pwd, 'Newpwd': new_pwd}
    try:
        res = post_pwd(url, msg)
        print(res)
    except Exception as e:
        # raise e
        res = json.loads(str(e))
        print('ModifyPwdError:', e)
    return json.dumps(res.decode())


class ResetPwdView(View):
    def post(self, request, *args, **kwargs):
        u_name = request.POST.get('name')
        u_pwd = request.POST.get('pwd')
        url = 'http://10.126.11.124:9000/user/reset_password'
        msg = {'Name': u_name, 'Newpwd': u_pwd}
        print(msg)
        try:
            res = post_pwd(url, msg)
            print(json.dumps(res.decode()))
        except Exception as e:
            res = json.loads(str(e))
            print('ResetPwdError:', e)
        return HttpResponse(json.dumps(res.decode()))
