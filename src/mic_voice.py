# -*- coding:utf-8 -*-
import logging
from utils.snowboy import snowboydecoder
import sys
import signal
import os
from config.path import WAVE_DING, WAVE_DONG, HOTWORD_MODELS
from time import sleep
import hashlib
from src.tts import TTSEngine

class Mic:
    """
    处理语音输出和输入
    """

    def __init__(self):
        self._logger = logging.getLogger()
        self.passive_interrupted = False
        self.tts_engine = TTSEngine()

    def passive_listen(self):
        """
        监听唤醒热词
        :param PERSONA:
        :return:
        """

        def signal_handler(signal, frame):
            self.passive_interrupted = True
            detector.terminate()
            sys.exit()

        def interrupt_callback():
            """
            检测到中断怎么办
            :return:
            """
            return self.passive_interrupted

        def detected_callback():
            """
            监听到热词怎么办
            :return:
            """
            self.play(WAVE_DING)
            self._logger.info('Hotword Detected.')
            detector.terminate()

        # capture SIGINT signal, e.g., Ctrl+C
        signal.signal(signal.SIGINT, signal_handler)

        detector = snowboydecoder.HotwordDetector(HOTWORD_MODELS, sensitivity=0.5)
        print('Listening Hotword... Press Ctrl+C to exit')

        # main loop
        detector.start(detected_callback=detected_callback,
                       interrupt_check=interrupt_callback,
                       sleep_time=0.03)

        return True, "DINGDANG"

    def active_listen(self):
        """
        持续录音，直到声音停止1秒，或者达到录音超时时间
        :return:
        """
        sleep(1.5)
        self.play(WAVE_DONG)

    def say(self, phrase):
        """
        TTS输出内容
        :param phrase:
        :return:
        """
        is_tts_cached, cache_file_path = self.tts_engine.get_speech_cache(phrase)
        if is_tts_cached:
            self._logger.info('Play cached wave file %s.', is_tts_cached)
            self.play(cache_file_path)
        else:
            print("DINGDANG: %s" % phrase)

    def play(self, src):
        """
        播放一段音频
        :param src:
        :return:
        """
        os.system('play %s' % src)





