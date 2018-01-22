# -*- coding: utf-8-*-
import datetime as dt
import pytz
from src.plugins import is_all_word_segment_in_text
import socket

WORDS = ["IP地址", "IP", "网络地址", 'ip', 'ip地址']


def __get_host_ip():
    """
    获取本机IP地址
    :return:
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def handle(text, mic, profile, iot_client=None,chatbot=None):
    mic.say("我的IP地址是 "+__get_host_ip())


def is_valid(text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return is_all_word_segment_in_text(WORDS, text)
