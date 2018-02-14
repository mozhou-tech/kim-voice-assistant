# -*- coding: utf-8-*-
import logging
import requests
import json
import random,math

WORDS = ["你是谁", "你是做啥的"]  #  kim的自我介绍
PRIORITY = 0
logger = logging.getLogger()
from src.plugins import is_all_word_segment_in_text


def handle(text, mic, profile, iot_client=None, chatbot=None):
    """
    处理
    :param text:
    :param mic:
    :param profile:
    :param iot_client:
    :return:
    """
    mic.say('我是您的私人助理，kim')


def is_valid(text):
    return is_all_word_segment_in_text(WORDS, text)

