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
import json, re
from config.path import APP_PATH


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
        # self._mqtt_client.do_connect()
        t = Thread(target=self._mqtt_client.do_connect, daemon=True)  # 启动一个线程，监听
        t.start()
        time.sleep(1)           # 等待mqtt连接服务器成功

    def test_publish_message(self):
        """
        发送消息
        :return:
        """
        self._logger.info('testing publish message.')
        self._mqtt_client.do_publish(topic_name='fc_asr', payload=b'hello world')
        self._mqtt_client.do_subscribe(topic_name='fc_asr')
        time.sleep(1)
        self._mqtt_client.do_disconnect()

    def atest_shadow_update(self):
        """
        获取设备影子数据
        :return:
        """
        with open(APP_PATH+'/utils/aliyun_iotx/resource/device_shadow.json') as f:
            json_data = re.sub('\s', '', f.read())

        self._logger.info('testing update shadow.')
        self._mqtt_client.do_shadow_update(json_data)
        self._mqtt_client.do_subscribe('fc_tts')
        time.sleep(2)
        # while True:
        #     pass
        self._mqtt_client.do_disconnect()


if __name__ == '__main__':
    logger.init(info=True)
    unittest.main()


