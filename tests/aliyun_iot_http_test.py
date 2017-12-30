# -*- coding: utf-8-*-
import unittest
import os
os.sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from utils.aliyun_iotx.iot_mqtt_client import IotClient
from config import profile
from utils import logger
import logging
import requests
from utils.aliyun_iotx.sign import Sign


class TestAliyunIot(unittest.TestCase):
    """

    """
    def test_init(self):
        self._logger = logging.getLogger()

    def test_sign(self):
        """签名方法测试"""
        sign_str = Sign.get_sign('aaa', 'bbb', 'aaa')


    def test_mqtt_client(self):
        # client.on_connect = on_connect
        # client.on_message = on_message
        # mqttc = mqtt.Client(self.mqtt_url)
        iot_client = IotClient.get_instance()
        iot_client.connect_mqtt()






if __name__ == '__main__':
    logger.init(info=True)
    unittest.main()

