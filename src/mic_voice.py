# -*- coding:utf-8 -*-
import logging
from utils.snowboy import snowboydecoder
import sys
import signal
import os
from config.path import WAVE_DING, WAVE_DONG, HOTWORD_MODELS, CACHE_WAVE_RECORDED
from src.tts import TTSEngine
import wave, pyaudio, audioop
import time


class Mic:
    """
    处理语音输出和输入
    """

    def __init__(self):
        self._logger = logging.getLogger()
        self.passive_interrupted = False
        self.tts_engine = TTSEngine()
        self._audio = pyaudio.PyAudio()
        self._logger.info("Initialization of PyAudio completed.")

    def __del__(self):
        self._audio.terminate()

    def _get_score(self, data):
        rms = audioop.rms(data, 2)
        score = rms / 3
        return score

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

    def active_listen(self, threshold = None):
        """
        持续录音，直到声音停止1秒，或者达到录音超时时间 12s
        :return:
        """
        self._audio.get_default_input_device_info()
        chunk = 1024
        wave_format = pyaudio.paInt16
        channels = 2
        rate = 44100
        record_seconds = 12         # 录音持续时间

        stream = self._audio.open(format=wave_format,
                                  channels=channels,
                                  rate=rate,
                                  input=True,
                                  frames_per_buffer=chunk)

        self._logger.info("active listen recording")

        frames = []

        # stores the lastN score values
        last_n = [i for i in range(20)]
        low_volume_count = 0        # 记录沉默持续时间（较安静时）
        for i in range(0, int(rate / chunk * record_seconds)):
            data = stream.read(chunk)
            frames.append(data)   # 添加到音频流

            last_n.pop(0)       # save this data point as a score
            last_n.append(self._get_score(data))
            if threshold is None or max(last_n) > threshold:        # 寻找最大值
                threshold = max(last_n)

            average = sum(last_n) / len(last_n)             # 当前循环中声音评分的平均值
            self._logger.info('average:%s, threshold:%s', average, threshold)

            # 采样声音的最大值突破100时，开始检测
            if threshold > 100:
                if average < 80:
                    low_volume_count = low_volume_count + 1
                if average > 100:               # 如果有声音，就清空周期计数
                    low_volume_count = 0
                if low_volume_count >= 38:      # 等待周期数
                    break

        self.play(WAVE_DONG)
        self._logger.info("active listen done recording")

        stream.stop_stream()
        stream.close()
        wf = wave.open(CACHE_WAVE_RECORDED, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(self._audio.get_sample_size(wave_format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()

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





