# -*- coding:utf-8 -*-
import os
import hashlib
from config.path import CACHE_WAVE_PATH
import logging
from utils.aliyun_iotx.iot_mqtt_client import IotClient


class TTSEngine:
    """
    语音合成
    """
    def __init__(self, over_iothub=True):
        self._logger = logging.getLogger()
        self._iot_client = IotClient.get_instance()

    @classmethod
    def get_instance(cls):
        """
        返回一个TTS示例
        :return:
        """
        return TTSEngine()

    def get_speech_cache(self, phrase, auto_cache=False):
        """
        语音文件会以对应文本的md5加密后命名，在做语音转换时，优先从缓存取出
        :param phrase:
        :return:
        """
        cache_file = CACHE_WAVE_PATH + 'tts_' + hashlib.md5(phrase.encode('utf8')).hexdigest()+'.wav'
        self._logger.info('look cache.')
        if os.access(cache_file, os.R_OK):
            return True, cache_file    # 找到对应的缓存并返回文件路径
        else:
            return False, cache_file   # 没有找到缓存

    def fetch_speech_wave(self, phrase):
        """
        获取语音wav文件，并放到缓存目录
        :param phrase:
        :return:
        """



