# -*- coding: utf-8-*-
import unittest
import os
os.sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.tts import TTSEngine
from utils import logger
from utils.aliyun_iotx.iot_mqtt_client import IotClient
from threading import Thread


class TestTTSEngine(unittest.TestCase):
    """

    """

    def setUp(self):
        self.iot_client = IotClient.get_instance()
        Thread(target=self.iot_client.do_connect, daemon=True).start()   # 建立IoTHub监听进程
        self.tts_engine = TTSEngine(self.iot_client)

    def test_test(self):
        print(self.tts_engine)


if __name__ == '__main__':
    logger.init(info=True)
    unittest.main()

