# -*- coding: utf-8 -*-
import hashlib
import hmac
import base64
import requests
import urllib
import datetime
import ssl


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

    client = http_proxy(ak_id='LTAIsk0qFRkhyL2Q', ak_secret='xi7FP7EFafFV3CNUO0G2HAOzvSRAPi')
    return client.send_request('https://nlsapi.aliyun.com/speak?encode_type=wav', '你好')