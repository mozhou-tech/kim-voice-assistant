# -*- coding: utf-8-*-
import unittest
import os,jieba
os.sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.plugins import Weather,WakeUpBell
from utils import logger
from src import mic_text
from config.path import APP_RESOURCES_DATA_PATH
from src import mic_voice
import requests


class TestSrcPlugins(unittest.TestCase):
    """

    """
    def setUp(self):
        jieba.set_dictionary(APP_RESOURCES_DATA_PATH + 'jieba.dict')  # 设置中文分词库

    def atest_weather(self):
        """
        获取天气数据
        """
        text = '后天天气预报'
        if Weather.isValid(text):
            Weather.handle(text=text, mic=mic_text.Mic(), profile='小云')

    def test_wakeup_bell(self):
        text = '起床叫我吧'
        if WakeUpBell.isValid(text):
            WakeUpBell.handle(text=text, mic=mic_text.Mic(), profile='小云')


if __name__ == '__main__':
    logger.init(info=True)
    unittest.main()

