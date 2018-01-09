# -*- coding: utf-8-*-
import unittest
import os
os.sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.tts import TTSEngine
from utils import logger
from threading import Thread
from time import sleep
from src.mic_voice import Mic


class TestMicVoiceEngine(unittest.TestCase):
    """

    """

    def setUp(self):
        self.mic = Mic()

    def test_say(self):
        """
        测试获取语音
        :return:
        """
        self.mic.say('你好柯良妹')



if __name__ == '__main__':
    logger.init(info=True)
    unittest.main()

