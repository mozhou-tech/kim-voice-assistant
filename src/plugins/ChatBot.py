# -*- coding: utf-8-*-
import random
import aliyunsdkchatbot

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
    return_text = chatbot.send_message(text)
    mic.say(return_text)


def is_valid(text):
    return True
