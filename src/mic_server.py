# -*- coding: utf-8-*-
import logging
from config import profile
from src.mic_base import MicBase

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
        self._logger.info("小云(发送到服务端): " + phrase)


