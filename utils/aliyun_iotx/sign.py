# -*- coding:utf-8 -*-

import hashlib
import urllib.request
import hmac
import base64
import datetime
import logging
import ssl
import pytz
from config import profile
import time
import uuid


class Sign:
    """
    签名类
    """

    def __init__(self, device_name, device_secret, product_key):
        self.device_name = device_name
        self.device_secret = device_secret
        self.product_key = product_key
        self._logger = logging.getLogger()


    def __md5_base64(self, strbody):
        hash = hashlib.md5()
        hash.update(strbody.encode('utf-8'))
        return base64.b64encode(hash.digest()).decode('utf-8')

    def __hmac_sha1(self, str_to_sign, secret):
        hmacsha1 = hmac.new(secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha1)
        return base64.b64encode(hmacsha1.digest()).decode('utf-8')

    def __get_timestamps(self):
        """
        获取当前时间戳
        :return:
        """
        timestamp = str(time.time())
        return timestamp

    def __get_client_id(self):
        """
        获取设备MAC地址
        :return:
        """
        node = uuid.getnode()
        return uuid.UUID(int=node).hex[-12:]

    @classmethod
    def get_sign(cls, device_name, device_secret, product_key, signmethod="hmacsha1"):
        """
        获取签名
        :param content:
        :param sign_method:
        :param device_secret:
        :return:
        """
        cls.obj = Sign(device_name, device_secret, product_key)
        mqtt_timestamps = cls.obj.__get_timestamps()
        mqtt_client_id = cls.obj.__get_client_id()+"|securemode=3,signmethod="+\
                         signmethod+",timestamp="+mqtt_timestamps+"|"
        content = ''.join(sorted([product_key, device_name, mqtt_client_id, mqtt_timestamps]))
        cls.obj._logger.info(content)
        sign_str = cls.obj.__hmac_sha1(device_secret, content)
        cls.obj._logger.info('generate sign %s', sign_str)
        return sign_str






