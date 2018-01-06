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
        hash.update(strbody.encode('utf-8'))
        self._logger.info('mdtbase64 strbody %s', strbody)
        self._logger.info('mdtbase64 strbody md5 %s', hash.digest())
        # if isinstance(strbody, bytes):
        #     hash.update(strbody)
        # else:
        #     hash.update(strbody.encode('utf-8'))
        return base64.b64encode(hash.digest()).decode('utf-8')

    def __sha1_base64(self, str_to_sign, secret):
        hmacsha1 = hmac.new(secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha1)
        return base64.b64encode(hmacsha1.digest()).decode('utf-8')

    def send_request_for_tts(self, url, body):
        """
        发送转换请求
        :param url:
        :param body:
        :return:
        """
        gmtnow = self.__current_gmt_time()
        body_md5 = self.__md5_base64(body)
        str_to_sign = "POST\napplication/json\n" + body_md5 + "\napplication/json\n" + gmtnow
        signature = self.__sha1_base64(str_to_sign, self.__ak_secret)
        auth_header = "Dataplus " + self.__ak_id + ":" + signature
        data = body.encode('utf-8')

        return requests.post(url=url, data=data, headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Date": gmtnow,
            "Authorization": auth_header
        }).content

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

    params = json.loads(event)
    if not params.get('type'):
        params = {
            'type': 'asr',
            'wave_bytes': 'abc'
        }
    client = http_proxy(ak_id=appsecret['ak_id'], ak_secret=appsecret['ak_secret'])
    # 文字转语音
    if params['type'] == 'tts':
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
        return client.send_request_for_tts('https://nlsapi.aliyun.com/speak?' +
                                           'encode_type='+params['encode_type'] +
                                           '&voice_name=' + params['voice_name'] +
                                           '&speech_rate=120'
                                           '&volume=60'
                                           '&sample_rate=16000'
                                           ,
                                           params['text'].strip())
    # 语音识别
    elif params['type'] == 'asr':
        # wave_bytes = base64.b64decode(params['wave_bytes'].encode('utf-8'))
        wave_bytes = 'asdfasdf'
        return client.send_request_for_asr('https://nlsapi.aliyun.com/recognize?model=chat&version=2.0'
                                           ,
                                           wave_bytes
                                           )
    else:
        raise Exception('Unsupported type.')
