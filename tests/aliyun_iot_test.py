# -*- coding: utf-8-*-
import unittest
import os
os.sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from utils.aliyun_iotx_mqtt import client
from config import profile
from utils import logger
import logging


class TestAliyunIot(unittest.TestCase):
    """

    """
    def test_init(self):
        self._logger = logging.getLogger()
        """
        准备客户端要求的参数
        """
        self.auth_url = "https://iot-auth.cn-shanghai.aliyuncs.com/auth/devicename"
        # 设备key和secret信息
        self.device_name = ""
        self.product_key = ""
        self.device_secret = ""
        # MQTT地址
        self.mqtt_url = self.product_key + ".iot-as-mqtt.cn-shanghai.aliyuncs.com:1883"
        # 用于测试的Topic
        self.sub_topic = "/" + self.product_key + "/" + self.device_name + "/get"
        self.pub_topic = "/" + self.product_key + "/" + self.device_name + "/update"
        # 设备影子topic
        self.shadow_ack_topic = "/shadow/get/" + self.product_key + "/" + self.device_name
        self.shadow_update_topic = "/shadow/update/" + self.product_key + "/" + self.device_name
        self.shadow_version = 0

    def test_simple_client(self):
        pass




if __name__ == '__main__':
    logger.init(info=True)
    unittest.main()

