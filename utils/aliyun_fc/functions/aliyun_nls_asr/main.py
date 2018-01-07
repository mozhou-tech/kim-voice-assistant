# -*- coding: utf-8 -*-
import hashlib
import hmac
import base64
import requests
import urllib
import datetime
import ssl
import json
import re
import base64
import logging

class http_proxy:
    """
    Http工具类，封装了鉴权
    """

    def __init__(self, ak_id, ak_secret):
        self.__ak_id = ak_id
        self.__ak_secret = ak_secret
        self._logger = logging.getLogger()

    def __current_gmt_time(self):
        date = datetime.datetime.strftime(datetime.datetime.utcnow(), "%a, %d %b %Y %H:%M:%S GMT")
        return date

    def __md5_base64(self, strbody):
        hash = hashlib.md5()
        hash.update(strbody)
        # hash.update(strbody.encode('utf-8'))
        self._logger.info('mdtbase64 strbody %s', strbody)
        self._logger.info('mdtbase64 strbody md5 %s', hash.digest())
        return base64.b64encode(hash.digest()).decode('utf-8')

    def __sha1_base64(self, str_to_sign, secret):
        hmacsha1 = hmac.new(secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha1)
        return base64.b64encode(hmacsha1.digest()).decode('utf-8')

    def send_request_for_asr(self, url, body):
        """
        asr
        :param url:
        :param body:
        :return:
        """
        gmtnow = self.__current_gmt_time()
        body_md5 = self.__md5_base64(body)
        self._logger.info('body_md5 %s:', body_md5)
        str_to_sign = "POST\napplication/json\n" + body_md5 + "\naudio/wav; samplerate=16000\n" + gmtnow
        signature = self.__sha1_base64(str_to_sign, self.__ak_secret)
        self._logger.info('signature %s:', signature)
        auth_header = "Dataplus " + self.__ak_id + ":" + signature

        return requests.post(url=url, data=body, headers={
            "Accept": "application/json",
            "Content-Type": "audio/wav; samplerate=16000",
            "Date": gmtnow,
            "Authorization": auth_header,
            "Content-Length": str(len(body))
        }).content


def my_handler(event, context):
    """
    入口函数
    :param event:
    :param context:
    :return:
    """
    with open("appsecret.json", 'r') as f:    # 从json中读取ak信息
        appsecret = json.loads(f.read())
    client = http_proxy(ak_id=appsecret['ak_id'], ak_secret=appsecret['ak_secret'])
    return client.send_request_for_asr('https://nlsapi.aliyun.com/recognize?model=chat&version=2.0', event)
