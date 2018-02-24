# -*- coding: utf-8-*-

from src.components.snowboy import snowboydecoder
import sys
import signal
from config import snowboy
import logging


class Detector():
    """
    唤醒词监听
    """
    def __init__(self):
        self._logger = logging.getLogger()
        self._logger.info("Initializing HotWord Detector.")

        self.interrupted = False
        signal.signal(signal.SIGINT, self.signal_handler)


    def signal_handler(self, signal, frame):
        self.interrupted = True

    def interrupt_callback(self):
        return self.interrupted

    def main(self):
        detector = snowboydecoder.HotwordDetector(snowboy.detect_model, sensitivity=0.5)
        print('Listening... Press Ctrl+C to exit')

        # main loop
        detector.start(detected_callback=snowboydecoder.play_audio_file,
                       interrupt_check=self.interrupt_callback,
                       sleep_time=0.03)
        detector.terminate()





