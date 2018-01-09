# -*- coding: utf-8-*-
import unittest
import os
os.sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.plugins import Weather
from utils import logger
from src import mic_text


class TestSrcPlugins(unittest.TestCase):
    """

    """

    def test_weather(self):
        """
        获取天气数据
        """
        result = Weather.handle(text='南京', mic=mic_text.Mic())
        print(result)


if __name__ == '__main__':
    logger.init(info=True)
    unittest.main()

