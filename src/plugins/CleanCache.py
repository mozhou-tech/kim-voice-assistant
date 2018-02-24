# -*- coding: utf-8-*-
import logging,shutil,os
WORDS = ["清空缓存", '清缓存']
PRIORITY = 0
logger = logging.getLogger()
from src.plugins import is_all_word_segment_in_text
from src.config.path import CACHE_WAVE_PATH


def handle(text, mic, profile, iot_client=None, chatbot=None):
    """
        Reports the current time based on the user's timezone.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
        wxBot -- wechat robot
    """
    shutil.rmtree(CACHE_WAVE_PATH)
    os.mkdir(CACHE_WAVE_PATH)
    mic.say('缓存已清空')


def is_valid(text):
    return is_all_word_segment_in_text(WORDS, text)
