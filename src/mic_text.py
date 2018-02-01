# -*- coding: utf-8-*-
import logging
from config import profile
from src.mic_base import MicBase
from utils import logger

mic_name = 'text'


class Mic(MicBase):
    """
    处理文本输出和输入
    """
    def __init__(self, iot_client):
        MicBase.__init__(self)
        self.iot_client = iot_client
        self.is_server_listen_thread = False

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
        input_content = input("我: ")
        logger.send_conversation_log(iot_client=self.iot_client, mic=mic_name, content='我：'+input_content)
        return input_content

    def say(self, phrase):
        """
        输出内容
        :param phrase:
        :return:
        """
        say_str = "小云: " + phrase
        print(say_str)
        logger.send_conversation_log(iot_client=self.iot_client, mic=mic_name, content=say_str)


