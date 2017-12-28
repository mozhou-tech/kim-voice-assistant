# -*- coding:utf-8 -*-

import json
from utils.aliyun_qas_sdk.http_proxy import http_proxy

ak_id = "LTAIsk0qFRkhyL2Q"
ak_secret = "xi7FP7EFafFV3CNUO0G2HAOzvSRAPi"
url = "https://nlsapi.aliyun.com/manage/qas"

if __name__ == '__main__':
    action = "projects:list"
    body = {"projectId":1, "themeId":123, "offset":0, "pageSize":20}
    jsonbody = json.dumps(body).replace(' ', '')
    
    proxy = http_proxy(ak_id, ak_secret)
    url = url + "?action=" + action
    result = proxy.send_request(url, jsonbody)
    print(result)