# -*- coding: utf-8-*-
import logging
from utils.aliyun_iotx.sign import Sign
import requests


class IotClient:

    def __init__(self):
        self._logger = logging.getLogger()
        """
        准备客户端要求的参数
        """
        self.endpoint = "https://iot-as-http.cn-shanghai.aliyuncs.com"
        self.path = ""
        # 设备key和secret信息
        self.device_name = "xiaoyun001"
        self.product_key = "5ixlFmlsHNI"
        self.device_secret = "iuaUl6Z7BYnrdumO9jSIk3syzquEm7GK"


    def build_data(self, hmacsha1='hmacsha1'):
        """
        构建请求header
        :param hmacsha1:
        :return:
        """
        origin = {
            "deviceName" : self.device_name,
            "productKey": self.product_key
        }
        signData = Sign.get_sign(params=origin, device_secret=self.device_secret, signmethod=hmacsha1)
        return dict(origin, **{
            "version": "default",
            "clientId": signData['iot_client_id'],
            "signmethod": hmacsha1,
            "sign": signData['sign'],
            "timestamp": signData['timestamp']
        })

    def auth(self):
        """
        获得iotToken
        :return:
        """
        self.path = '/auth'
        url = self.endpoint + self.path
        json_data = self.build_data()
        self._logger.info('Post request %s', url)
        self._logger.info('Post auth data %s', json_data)
        r = requests.post(url=url, json=json_data, headers={
            "Content-Type": "application/json",
        })
        self._logger.info(r.text)


    @classmethod
    def get_instance(cls):
        return IotClient()

