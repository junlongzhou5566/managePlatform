# -*- coding: utf-8 -*-
from aliyun_api_gateway_sign_py3.com.aliyun.api.gateway.sdk import client
from aliyun_api_gateway_sign_py3.com.aliyun.api.gateway.sdk.http import request
from aliyun_api_gateway_sign_py3.com.aliyun.api.gateway.sdk.common import constant
import json

host = "https://test.co"
url = "/get_ali_oss_token?bucket=sds"

cli = client.DefaultClient(app_key="appkey", app_secret="app_secret")
req_post = request.Request(host=host, protocol=constant.HTTP, url=url, method="GET", time_out=30000)
req_post.set_content_type(constant.CONTENT_TYPE_FORM)
body_map = {"bodyForm1": "fwefwef", "bodyForm2": "ffwefwef"}
req_post.set_body(body_map)
res = cli.execute(req_post)
if res and res[0] and int(res[0]) == 200:
    data_str = res[2]
    data = json.loads(data_str)
    print(data)
