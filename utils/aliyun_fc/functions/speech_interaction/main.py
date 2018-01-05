# -*- coding: utf-8 -*-
import hashlib
import hmac
import base64
import requests
import urllib
import datetime
import ssl
import json


class http_proxy:
    """
    Http工具类，封装了鉴权
    """

    def __init__(self, ak_id, ak_secret):
        self.__ak_id = ak_id
        self.__ak_secret = ak_secret

    def __current_gmt_time(self):
        date = datetime.datetime.strftime(datetime.datetime.utcnow(), "%a, %d %b %Y %H:%M:%S GMT")
        return date

    def __md5_base64(self, strbody):
        hash = hashlib.md5()
        hash.update(strbody.encode('utf-8'))
        print(hash.digest())
        return base64.b64encode(hash.digest()).decode('utf-8')

    def __sha1_base64(self, str_to_sign, secret):
        hmacsha1 = hmac.new(secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha1)
        return base64.b64encode(hmacsha1.digest()).decode('utf-8')

    def send_request(self, url, body):
        gmtnow = self.__current_gmt_time()
        print(gmtnow)
        body_md5 = self.__md5_base64(body)
        print(body_md5)
        str_to_sign = "POST\napplication/json\n" + body_md5 + "\napplication/json\n" + gmtnow
        print(str_to_sign)
        signature = self.__sha1_base64(str_to_sign, self.__ak_secret)
        print(signature)
        auth_header = "Dataplus " + self.__ak_id + ":" + signature
        print(auth_header)

        ssl._create_default_https_context = ssl._create_unverified_context
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/json")
        req.add_header("Content-Type", "application/json")
        req.add_header("Date", gmtnow)
        req.add_header("Authorization", auth_header)

        data = body.encode('utf-8')
        f = urllib.request.urlopen(req, data)
        return f.read()


def my_handler(event, context):
    """
    入口函数
    :param event:
    :param context:
    :return:
    """
    with open("appsecret.json", 'r') as f:    # 从json中读取ak信息
        appsecret = json.loads(f.read())
    params = json.loads(event)

    # 准备参数encode_type
    if 'encode_type' not in params or params['encode_type'] is None:
        params['encode_type'] = 'wav'

    # 使用男声还是女声
    if 'voice_name' not in params or params['voice_name'] not in ['xiaogang', 'xiaoyun', 'man', 'woman']:
        params['voice_name'] = 'xiaogang'
    elif params['voice_name'] == 'woman':
        params['voice_name'] = 'xiaoyun'
    else:
        params['voice_name'] = 'xiaogang'

    client = http_proxy(ak_id=appsecret['ak_id'], ak_secret=appsecret['ak_secret'])
    return client.send_request('https://nlsapi.aliyun.com/speak?' +
                               'encode_type='+params['encode_type'] +
                               '&voice_name=' + params['voice_name'] +
                               '&speech_rate=120'
                               '&volume=60'
                               '&sample_rate=16000'
                               ,
                               params['text'])
