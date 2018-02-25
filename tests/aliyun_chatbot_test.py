# -*- coding: utf-8-*-
import unittest
import os
from src.components import logger
import logging
from src.components.aliyun_fc.fc_client import FcClient
import json
import wave
import time
from src.config.path import CACHE_WAVE_PATH
from src.components.chatbot import Chatbot


class TestAliyunFc(unittest.TestCase):
    """
    函数计算单元测试
    """
    def setUp(self):
        self._logger = logging.getLogger()
        self.fc_client = FcClient.get_instance()

    def test_send_message(self):
        chatbot = Chatbot.get_instance()
        msg = chatbot.send_message('你是谁哈')
        print(msg)


if __name__ == '__main__':
    logger.init(info=True)
    unittest.main()


