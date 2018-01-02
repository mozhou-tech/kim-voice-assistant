# -*- coding: utf-8-*-
import unittest
import os
os.sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from utils.aliyun_iotx.iot_http_client import IotClient
from config import profile
from utils import logger
import logging
import requests
from utils.aliyun_iotx.sign import Sign


class TestAliyunIot(unittest.TestCase):

    def test_auth(self):
        iot_client = IotClient.get_instance()
        iot_client.get_auth_token()

    def test_device_data_pub(self):
        iot_client = IotClient.get_instance()
        iot_client.publish_msg('messagebody')


if __name__ == '__main__':
    logger.init(info=True)
    unittest.main()

