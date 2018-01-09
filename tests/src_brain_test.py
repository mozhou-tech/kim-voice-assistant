# -*- coding: utf-8-*-
import unittest
import os
os.sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from utils import logger
from src.mic_voice import Mic
from src.brain import Brain
import jieba


class TestMicVoiceEngine(unittest.TestCase):
    """

    """

    def setUp(self):
        pass

    def test_get_plugins(self):
        """
        获取插件
        :return:
        """
        plugins = Brain.get_plugins()
        print(jieba.cut('获取插件', cut_all=True))


if __name__ == '__main__':
    logger.init(info=True)
    unittest.main()

