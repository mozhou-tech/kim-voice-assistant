# -*- coding:utf-8 -*-
import os
import hashlib
from config.path import CACHE_WAVE_PATH
import logging
from utils.aliyun_fc.fc_client import FcClient
import time


class TTSEngine:
    """
    语音合成
    """
    def __init__(self, fc_client):
        self._logger = logging.getLogger()
        self._fc_client = fc_client


    @classmethod
    def get_instance(cls):
        """
        返回一个TTS示例
        :return:
        """
        return TTSEngine(FcClient.get_instance())

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
        start_time = time.time()
        self._logger.info('Fetch speech wave from aliyun fc.')
        payload = {'text': phrase}
        b, wave_pathname = self.get_speech_cache(phrase=phrase)
        result = self._fc_client.call_function('aliyun_nls_tts', payload=payload)
        if result.headers['Content-Type'] == 'application/octet-stream':
            with open(wave_pathname, 'wb') as f:
                f.write(result.data)
        end_time = time.time()
        self._logger.info('Get wave success, use time %ss', round(end_time-start_time, 3))
        return wave_pathname




