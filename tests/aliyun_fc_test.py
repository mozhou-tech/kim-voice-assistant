# -*- coding: utf-8-*-
import unittest
import os
os.sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from utils import logger
import logging
import time
from utils.aliyun_fc.client import FcClient


class TestAliyunFc(unittest.TestCase):
    """
    函数计算单元测试
    """
    def setUp(self):
        self._logger = logging.getLogger()
        self.fc_client = FcClient.get_instance()

    def test_init_service(self):
        """
        检查函数计算服务是否已存在
        :return:
        """
        self.fc_client.create_fc_service()

    def test_update_functions(self):
        self.fc_client.update_functions('speech_interaction')

    def test_update_and_call_function_for_api_market(self):
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
        # result = self.fc_client.call_function('aliyun-api-market', payload=payload)
        # self._logger.info(result.data)

    def test_update_and_call_function_for_asr(self):
        """
        语音识别
        :return:
        """

    def test_update_and_call_function_for_tts(self):
        """
        语音合成
        :return:
        """
        return


if __name__ == '__main__':
    logger.init(info=True)
    unittest.main()


