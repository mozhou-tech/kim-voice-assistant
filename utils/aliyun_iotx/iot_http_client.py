# -*- coding: utf-8-*-
import logging
from utils.aliyun_iotx.sign import Sign


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




    @classmethod
    def get_instance(cls):
        return IotClient()

