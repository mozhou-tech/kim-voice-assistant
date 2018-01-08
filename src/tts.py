# -*- coding:utf-8 -*-
import os
import hashlib
from config.path import CACHE_WAVE_PATH
import logging


class TTSEngine:
    """
    语音合成
    """
    def __init__(self, over_iothub=True):
        self._logger = logging.getLogger()

    @classmethod
    def get_instance(cls):
        """
        返回一个TTS示例
        :return:
        """
        return TTSEngine()

    def get_speech_cache(self, phrase):
        """
        语音文件会以对应文本的md5加密后命名，在做语音转换时，优先从缓存取出
        :param phrase:
        :return:
        """
        cache_file = CACHE_WAVE_PATH + 'tts_' + hashlib.md5(phrase.encode('utf8')).hexdigest()+'.wav'
        self._logger.info('look cache.')
        if os.access(cache_file, os.R_OK):
            return True, cache_file
        else:
            return False, cache_file


