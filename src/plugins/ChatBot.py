# -*- coding: utf-8-*-
import random
import aliyunsdkchatbot
from src.config import load_yaml_settings

WORDS = []
PRIORITY = -99999


def handle(text, mic, profile, iot_client=None, chatbot=None):
    """
    内部实现完整的对话逻辑，对原来的逻辑无侵入
    :param text:
    :param mic:
    :param profile:
    :return:
    """
    if load_yaml_settings()['aliyun']['chatbot']['enable']:
        return_text = chatbot.send_message(text)
    else:
        return_text = random.choice([
            '你说啥，我不明白哈？',
            '宝宝没听懂',
            '我还不支持这个功能'
        ])
    mic.say(return_text)


def is_valid(text):
    return True
