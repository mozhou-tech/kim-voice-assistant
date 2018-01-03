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
import json
import fc2

class TestAliyunFc(unittest.TestCase):
    """
    函数计算单元测试
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

    def test_call_function_for_api_market(self):
        """
        调用函数计算服务，从API中读取数据
        :return:
        """
        # 获取天气预报的Payload
        payload = {
            'host': 'http://freecityid.market.alicloudapi.com',
            'path': '/whapi/json/alicityweather/briefforecast3days',
            'method': 'POST',
            'appcode': 'cd08e261838a42328340f49cd28c02b4',
            'payload': {
                'cityId': '1045'
            },
            'bodys': {},
            'querys': ''
        }
        # 获取新闻头条的Payload
        payload = {
            'host': 'http://topnews.market.alicloudapi.com',
            'path': '/toutiao/index',
            'method': 'GET',
            'appcode': 'cd08e261838a42328340f49cd28c02b4',
            'payload': {
                'type': 'top'
            },
            'bodys': {},
            'querys': ''
        }
        result = self.fc_client.invoke_function('xiaoyun-fc', 'aliyun-api-market', payload=json.dumps(payload))
        self._logger.info(result.data)


if __name__ == '__main__':
    logger.init(info=True)
    unittest.main()


