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


    # def test_sign(self):
    #     """签名方法测试"""
    #     iot_client = IotClient.get_instance()
    #     sign_str = Sign.get_sign(iot_client.device_name, iot_client.device_secret, iot_client.product_key)
    #     assert sign_str is not None

    # def test_build_data(self):
    #     iot_client = IotClient.get_instance()
    #     iot_client.build_data()

    def test_auth(self):
        iot_client = IotClient.get_instance()
        print(iot_client.get_auth_token())


if __name__ == '__main__':
    logger.init(info=True)
    unittest.main()

