# -*- coding:utf-8 -*-
import os
import hashlib
from config.path import CACHE_WAVE_PATH
import logging


class TTSEngine:
    def __init__(self):
        self._logger = logging.getLogger()

    def get_speech_cache(self, phrase):
        """
        语音文件会以对应文本的md5加密后命名，在做语音转换时，优先从缓存取出
        :param phrase:
        :return:
        """
        cache_file = CACHE_WAVE_PATH + hashlib.md5(phrase.encode('utf8')).hexdigest()+'.wav'
        self._logger.info('look cache.')
        if os.access(cache_file, os.R_OK):
            return True, cache_file
        else:
            return False, cache_file


