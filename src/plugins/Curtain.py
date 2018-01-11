# -*- coding: utf-8-*-
import logging
import jieba

WORDS = [u"窗帘"]
PRIORITY = 1
from src.plugins import is_all_word_segment_in_text


def handle(text, mic, profile):
    """
        Reports the current time based on the user's timezone.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    if any(word in text for word in ["打开", "开启"]):
        text = u"窗帘已打开"
    elif any(word in text for word in ["关闭", "关上"]):
        text = u"窗帘已关闭"
    else:
        text = u"窗帘还不支持该指令"
    mic.say(text)


def is_valid(text):
    return is_all_word_segment_in_text(WORDS, text)
