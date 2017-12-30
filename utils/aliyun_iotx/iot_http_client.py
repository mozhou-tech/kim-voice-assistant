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
        signData = Sign.get_sign(self.device_name, self.device_secret, self.device_secret, hmacsha1)
        return {
            "version": "default",
            "clientId": signData['iot_client_id'],
            "signmethod": hmacsha1,
            "sign": signData['sign'],
            "productKey": self.product_key,
            "deviceName": self.device_name,
            "timestamp": signData['timestamp']
        }

    def auth(self):
        """
        获得iotToken
        :return:
        """
        url = '/auth'
        r = requests.post(url=self.endpoint + url, data=self.build_data(), headers={
            "Content-Type": "application/json"
        })
        self._logger.info(r.text)


    @classmethod
    def get_instance(cls):
        return IotClient()

