# -*- coding: utf-8-*-
import logging
from config import profile
from src.mic_base import MicBase
from utils import logger
import requests,json

mic_name = 'server'


class Mic(MicBase):
    """
    处理文本输出和输入
    """
    def __init__(self, iot_client):
        MicBase.__init__(self)
        self._logger = logging.getLogger()
        self.iot_client = iot_client
        self.iot_client.do_subscribe(topic_name='mic_text_from_server')
        self._logger.info('MicServer监听进程初始化完成')
        self.is_server_listen_thread = True

    def passive_listen(self):
        """
        被动监听
        :return:
        """
        return True, profile.myname

    def active_listen(self):

        """
        主动监听
        :return:
        """
        pass

    def say(self, phrase):
        """
        输出内容
        :param phrase:
        :return:
        """
        input_content = "小云: " + phrase
        logger.send_conversation_log(iot_client=self.iot_client, mic=mic_name, content=input_content,
                                     speaker='device')
        self._logger.info(input_content)

        try:
            self._logger.info('send mic server message.')
            requests.post(url=profile.remote_control_service_endpoint, json={"data": {"message": input_content}})
        except:
            self._logger.info('request remote control service endpoint %s error: %s',
                              profile.remote_control_service_endpoint, r.text)


