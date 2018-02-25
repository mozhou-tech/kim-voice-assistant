# -*- coding: utf-8-*-
import unittest
import os
os.sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.components import logger
import logging
import json
import wave
import time
from src.config.path import CACHE_WAVE_PATH
from src.components.dingtalk import DingRobot


class TestDingtalk(unittest.TestCase):
    """
    函数计算单元测试
    """
    def setUp(self):
        pass

    def test_send_message(self):
        res = DingRobot.send_message(title='## 撒地方\n阿斯蒂芬', markdown_content='## 撒地方\n阿斯蒂芬')
        assert res is True


if __name__ == '__main__':
    logger.init(info=True, debug=True)
    unittest.main()


