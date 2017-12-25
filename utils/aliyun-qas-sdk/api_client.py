# -*- coding:utf-8 -*-

import json
from http_proxy import http_proxy

ak_id = "您自己的AccessKeyId"
ak_secret = "您自己的AccessKeySecret"
url = "https://nlsapi.aliyun.com/manage/qas"

if __name__ == '__main__':
    action = "projects:list"
    body = {"projectId":1, "themeId":123, "offset":0, "pageSize":20}
    jsonbody = json.dumps(body).replace(' ', '')
    
    proxy = http_proxy(ak_id, ak_secret)
    url = url + "?action=" + action
    result = proxy.send_request(url, jsonbody)
    print(result)