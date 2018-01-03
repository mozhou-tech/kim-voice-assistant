# -*- coding: utf-8-*-
import unittest
import os
os.sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from utils.aliyun_iotx.iot_mqtt_client import IotClient
from config import profile
from utils import logger
import logging
import time
import json
from config import profile
import fc2

class TestAliyunFc(unittest.TestCase):
    """

    """
    def setUp(self):
        self._logger = logging.getLogger()
        self.fc_client = fc2.Client(
            endpoint='https://1435638266713387.cn-shanghai.fc.aliyuncs.com',
            accessKeyID=profile.ak_id,
            accessKeySecret=profile.ak_secret)

    def test_list_service(self):
        # self.fc_client.create_service('xiaoyun-fc')
        services = self.fc_client.list_services()
        self._logger.info(services.data)

    def test_update_and_call_function(self):
        result = self.fc_client.invoke_function('xiaoyun-fc', 'aliyun-api-market', payload='啊是打发斯蒂芬'.encode('utf8'))
        self._logger.info(result.data)


if __name__ == '__main__':
    logger.init(info=True)
    unittest.main()


