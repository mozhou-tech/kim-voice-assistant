# -*- coding: utf-8-*-
import unittest
import os
os.sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.tts import TTSEngine
from src.components import logger
from threading import Thread
from time import sleep
from src.mic_voice import Mic


class TestMicVoiceEngine(unittest.TestCase):
    """

    """

    def setUp(self):
        self.mic = Mic()

    def atest_say(self):
        """
        测试获取语音
        :return:
        """
        self.mic.say('你好柯良妹')

    def test_listen(self):
        """
        测试监听和语音识别
        :return:
        """
        r = self.mic.listen('/Volumes/MacintoshHD/WorkHub/PycharmProjects/dingdang-robot/data/cache/wave/tts_1e40530cfbaab369b7315621429f8f6b.wav')
        print(r)

if __name__ == '__main__':
    logger.init(info=True)
    unittest.main()

