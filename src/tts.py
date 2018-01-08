# -*- coding:utf-8 -*-
import os
import hashlib
from config.path import CACHE_WAVE_PATH
import logging


class TTSEngine:
    """
    语音合成
    """
    def __init__(self, iot_client):
        self._logger = logging.getLogger()
        self._iot_client = iot_client
        self._iot_client.do_subscribe(topic_name='fc_tts')  # 订阅


    @classmethod
    def get_instance(cls, iot_client=None):
        """
        返回一个TTS示例
        :return:
        """
        return TTSEngine(iot_client)

    def get_speech_cache(self, phrase=None, phrase_md5=None, fetch_wave_on_no_cache=False):
        """
        语音文件会以对应文本的md5加密后命名，在做语音转换时，优先从缓存取出
        :param phrase:
        :param phrase_md5
        :param fetch_wave_on_no_cache 没有缓存时生成缓存，同时返回存储路径
        :return:
        """
        if phrase_md5 is None:
            if phrase is None:          # phrase和phrase_md5不能同时为None
                self._logger.error('phrase cannot be None.')
                return False, ''
            cache_file = CACHE_WAVE_PATH + 'tts_' + hashlib.md5(phrase.encode('utf8')).hexdigest()+'.wav'
        else:
            cache_file = CACHE_WAVE_PATH + phrase_md5 + '.wav'
        self._logger.info('look cache.')
        if os.access(cache_file, os.R_OK):
            return True, cache_file    # 找到对应的缓存并返回文件路径
        else:
            if fetch_wave_on_no_cache:   # 获取音频文件
                return True, self.fetch_speech_wave(phrase)
            else:
                return False, cache_file   # 没有找到缓存

    def fetch_speech_wave(self, phrase):
        """
        获取语音wav文件，并放到缓存目录
        :param phrase:
        :return: 返回wave存储路径
        """
        if self._iot_client is None:  # 使用aliyun IoTub
            return
        self._iot_client.do_publish(topic_name='fc_tts', payload=phrase)




