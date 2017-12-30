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

    def hmacsha1(self, content):
        content = bytes(content, 'utf8')
        hmacsha1 = hmac.new(bytes(self.device_secret, 'utf8'), content, hashlib.sha1)
        return hmacsha1.hexdigest()

    def __get_timestamps(self):
        """
        获取当前时间戳
        :return:
        """
        timestamp = str(int(time.time()*1000))
        return timestamp

    def __get_iot_client_id(self):
        """
        获取设备MAC地址
        :return:
        """
        node = uuid.getnode()
        return self.product_key + uuid.UUID(int=node).hex[-12:]

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
        timestamp = cls.obj.__get_timestamps()
        iot_client_id = cls.obj.__get_iot_client_id()
        content = ''.join(sorted([product_key, device_name, iot_client_id, timestamp]))
        cls.obj._logger.info(content)
        sign_str = cls.obj.hmacsha1(content)
        cls.obj._logger.info('generate sign %s', sign_str)
        return {
            'sign': sign_str,
            'signmethod': signmethod,
            'timestamp': timestamp,
            'iot_client_id': iot_client_id
        }






