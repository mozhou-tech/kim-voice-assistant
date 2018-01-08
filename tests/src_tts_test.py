# -*- coding: utf-8-*-
import unittest
import os
os.sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.tts import TTSEngine
from utils import logger
from utils.aliyun_iotx.iot_mqtt_client import IotClient
from threading import Thread
from time import sleep


class TestTTSEngine(unittest.TestCase):
    """

    """

    def setUp(self):
        self.iot_client = IotClient.get_instance()
        Thread(target=self.iot_client.do_connect, daemon=True).start()   # 建立IoTHub监听进程
        sleep(1)
        self.tts_engine = TTSEngine.get_instance(self.iot_client)

    def test_fetch_speech_wave(self):
        """
        测试获取语音
        :return:
        """
        result = self.tts_engine.fetch_speech_wave('你好世界')
        print(result)


if __name__ == '__main__':
    logger.init(info=True)
    unittest.main()

