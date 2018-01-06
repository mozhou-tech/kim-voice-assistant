# -*- coding:utf-8 -*-
import os
import hashlib
from config.path import CACHE_WAVE_PATH
import logging

class TTS_Engine:
    def __init__(self):
        self._logger = logging.getLogger()

    def has_speech_cache(self, phrase):
        """
        语音文件会以对应文本的md5加密后命名，在做语音转换时，优先从缓存取出
        :param phrase:
        :return:
        """
        cache_file = CACHE_WAVE_PATH + hashlib.md5(phrase.encode('utf8')).hexdigest()+'.wav'
        self._logger.info('检查是否存在TTS缓存文件%s', cache_file)
        if os.access(cache_file, os.R_OK):
            return cache_file
        else:
            return False


