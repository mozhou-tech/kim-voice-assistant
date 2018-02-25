# -*- coding: utf-8-*-
import logging
import requests
import json
import random,math

WORDS = ["你是谁", "你是做啥的", "自我介绍", "你叫什么", "kim"]  #  kim的自我介绍
PRIORITY = 0
logger = logging.getLogger()
from src.plugins import is_all_word_segment_in_text, plugin_output


def handle(text, mic, profile, iot_client=None, chatbot=None):
    """
    处理
    :param text:
    :param mic:
    :param profile:
    :param iot_client:
    :return:
    """
    plugin_output(text, mic, '我是基于阿里云创建的私人智能语音助理，KIM。')


def is_valid(text):
    return is_all_word_segment_in_text(WORDS, text)

