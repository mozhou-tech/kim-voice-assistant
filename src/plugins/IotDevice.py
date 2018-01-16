# -*- coding: utf-8-*-
import logging
import requests
import json
import random,math

WORDS = ["灯打开", '灯关闭', '灯关上', '打开窗帘', '关闭窗帘', '窗帘拉开', '窗帘拉上']
PRIORITY = 0
logger = logging.getLogger()
from utils.aliyun_iotx.iot_mqtt_client import IotClient
from config.path import APP_PATH
from utils import gpio_control
from src.plugins import is_all_word_segment_in_text


def handle(text, mic, profile):
    """
    物联网设备控制、MQTT
    :param text:
    :param mic:
    :param profile:
    :return:
    """
    if is_all_word_segment_in_text(['窗帘'], text):   # 窗帘控制
        if is_all_word_segment_in_text(['打开', '拉开'], text):
            mic.say('正在为您打开窗帘')
        elif is_all_word_segment_in_text(['关闭', '拉上'], text):
            mic.say('正在为你关闭窗帘')

    if is_all_word_segment_in_text(['灯'], text):       # 灯控制
        if is_all_word_segment_in_text(['打开'], text):
            mic.say('夜灯已打开')
        elif is_all_word_segment_in_text(['关闭', '关上'], text):
            mic.say('夜灯已关闭')


def is_valid(text):
    return is_all_word_segment_in_text(WORDS, text)

