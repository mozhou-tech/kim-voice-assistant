# -*- coding:utf-8 -*-

from http_proxy import http_proxy
import json

ak_id = "您自己的AccessKeyId"
ak_secret = "您自己的AccessKeySecret"
url = "https://nlsapi.aliyun.com/qas"

if __name__ == '__main__':
    prams = {"app_key":"nui-abcdefg","question":"你是谁？","version":"2.0"}
    body = json.dumps(prams).replace(' ', '')
    print(body)
    proxy = http_proxy(ak_id, ak_secret) 
    answer = proxy.send_request(url, body)
    print(answer)
