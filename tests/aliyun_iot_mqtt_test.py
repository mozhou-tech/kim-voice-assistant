# -*- coding: utf-8-*-
import unittest
import os
os.sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from utils.aliyun_iotx.iot_mqtt_client import IotClient
from config import profile
from utils import logger
import logging
from utils.aliyun_iotx.sign import Sign
from threading import Thread
import time


class TestAliyunIot(unittest.TestCase):
    """

    """
    def setUp(self):
        self._logger = logging.getLogger()
        self._mqtt_client = IotClient.get_instance()
        """
          mqtt连接
          :return:
          """
        # self._mqtt_client.connect_mqtt()
        t = Thread(target=self._mqtt_client.do_connect, daemon=True)  # 启动一个线程，监听
        t.start()
        time.sleep(1)           # 等待mqtt连接服务器成功

    def test_publish_message(self):
        self._logger.info('testing publish message.')
        self._mqtt_client.do_publish(payload=b'hello world')


if __name__ == '__main__':
    logger.init(info=True)
    unittest.main()

