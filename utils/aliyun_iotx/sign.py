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
        """
        HmacSha1算法 计算sign
        :param content:
        :return:
        """
        hmacsha1 = hmac.new(self.device_secret.encode('utf-8'), content.encode('utf-8'), hashlib.sha1)
        result = hmacsha1.hexdigest().upper()
        self._logger.info('Generate sign %s', result)
        return result

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
        result = self.product_key + uuid.UUID(int=node).hex[-12:].upper()
        self._logger.info('Generate client id %s', result.upper())
        return result.upper()

    @classmethod
    def get_sign(cls, params, device_secret, signmethod="hmacsha1"):
        """
        获取签名
        :param content:
        :param sign_method:
        :param device_secret:
        :return:
        """
        cls.obj = Sign(params['deviceName'], device_secret, params['productKey'])
        timestamp = cls.obj.__get_timestamps()
        iot_client_id = cls.obj.__get_iot_client_id()
        content = ''.join(sorted(['productKey'+params['productKey'],
                                  'deviceName'+params['deviceName'],
                                  'clientId'+iot_client_id,
                                  'timestamp'+timestamp]))
        cls.obj._logger.info('Sign content: %s', content)
        sign_str = cls.obj.hmacsha1(content)
        return {
            'sign': sign_str,
            'signmethod': signmethod,
            'timestamp': timestamp,
            'iot_client_id': iot_client_id
        }






