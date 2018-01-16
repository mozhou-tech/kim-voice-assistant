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
from src.plugins import is_all_word_segment_in_text


def handle(text, mic, profile):
    if is_all_word_segment_in_text(['窗帘'], text):   # 窗帘控制
        if is_all_word_segment_in_text(['打开', '拉开'], text):
            mic.say('窗帘已打开')
        elif is_all_word_segment_in_text(['关闭', '拉上'], text):
            mic.say('窗帘已关闭')

    if is_all_word_segment_in_text(['灯'], text):       # 灯控制
        if is_all_word_segment_in_text(['打开'], text):
            mic.say('夜灯已打开')
        elif is_all_word_segment_in_text(['关闭', '关上'], text):
            mic.say('夜灯已关闭')


def is_valid(text):
    return is_all_word_segment_in_text(WORDS, text)

