# -*- coding: utf-8-*-
import logging
import jieba
logger = logging.getLogger()
WORDS = [u"窗帘"]
PRIORITY = 1
from src.plugins import is_all_word_segment_in_text


def handle(text, mic, profile):
    """
    窗帘控制    打开窗帘、关闭窗帘
    :param text:
    :param mic:
    :param profile:
    :return:
    """

    if is_all_word_segment_in_text(["打开", "开启"], text):
        text = u"窗帘已打开"
    elif is_all_word_segment_in_text(["关闭", "关上"], text):
        text = u"窗帘已关闭"
    else:
        text = u"窗小帘还不支持该指令"
    mic.say(text)


def is_valid(text):
    return is_all_word_segment_in_text(WORDS, text)
