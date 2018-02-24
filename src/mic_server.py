# -*- coding: utf-8-*-
import logging
from src.config import profile
from src.mic_base import MicBase
from src.components import logger
import requests, json, os,threading
from src.tts import TTSEngine

mic_name = 'server'


class Mic(MicBase):
    """
    处理文本输出和输入
    """
    def __init__(self, iot_client, peer_mic=None):
        """
        :param iot_client:
        :param peer_mic: 与mic_server同时运行的监听,text或voice由 --textmode指定
        """
        MicBase.__init__(self)
        self._logger = logging.getLogger()
        self.iot_client = iot_client
        self.iot_client.do_subscribe(topic_name='mic_text_from_server')
        self._logger.info('MicServer监听进程初始化完成')
        self.is_server_listen_thread = True
        self._tts_engine = TTSEngine.get_instance()
        self._peer_mic = peer_mic

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
        input_content = phrase
        logger.send_conversation_log(iot_client=self.iot_client, mic=mic_name, content=input_content,
                                     speaker='device')
        self._logger.info(input_content)
        self._logger.info('send mic server message.')
        if self._peer_mic is not None:
            threading.Thread(target=self._peer_mic.say, args=(phrase,)).start()





