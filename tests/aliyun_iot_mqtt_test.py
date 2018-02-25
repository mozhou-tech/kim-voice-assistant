# -*- coding: utf-8-*-
import unittest
import os
os.sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.components.aliyun_iotx.iot_mqtt_client import IotClient
from src.config import profile
from src.components import logger
import logging
from src.components.aliyun_iotx.iot_mqtt_client import Sign
from threading import Thread
import time
import json, re
from src.config.path import APP_RESOURCES_DATA_PATH
from signal import pause


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
        self._mqtt_client.do_subscribe(is_shadow=True)

    def atest_publish_message(self):
        """
        发送消息
        :return:
        """
        self._logger.info('testing publish message.')
        publish_json = {
            'text': '随便转换一下'
        }
        self._mqtt_client.do_publish(topic_name='fc_tts', payload=json.dumps(publish_json))
        self._mqtt_client.do_subscribe(topic_name='fc_tts')
        time.sleep(10)
        self._mqtt_client.do_disconnect()

    def test_shadow_update_devstat(self):
        """
        获取设备影子数据
        :return:
        """
        self._mqtt_client.do_report_devstat(version_increase=True)
        print('x')
        time.sleep(10)
        # while True:
        #     pass

    def atest_get_devstat(self):
        self._mqtt_client.do_get_devstat()
        time.sleep(100)

    def tearDown(self):
        self._mqtt_client.do_disconnect()


if __name__ == '__main__':
    logger.init(info=True)
    unittest.main()


