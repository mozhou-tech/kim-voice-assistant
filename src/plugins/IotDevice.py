# -*- coding: utf-8-*-
import logging
import requests
import json
import random,math

WORDS = ["灯打开", '灯关闭', '灯关上', '打开窗帘', '关闭窗帘', '窗帘拉开', '窗帘拉上']
PRIORITY = 0
from config.path import APP_PATH
from utils.gpio_control import curtain, light
from src.plugins import is_all_word_segment_in_text


def handle(text, mic, profile, iot_client=None, chatbot=None):
    """
    物联网设备控制、MQTT
    :param text:
    :param mic:
    :param profile:
    :param iot_client
    :return:
    """
    curtain_device = curtain.Curtain.get_instance(iot_client)
    cmd = None
    if is_all_word_segment_in_text(['窗帘'], text):      # 窗帘控制
        if is_all_word_segment_in_text(['打开', '拉开'], text):
            cmd = 'open'
            mic.say('正在为您打开窗帘')
        elif is_all_word_segment_in_text(['关闭', '拉上'], text):
            cmd = 'close'
            mic.say('正在为你关闭窗帘')
        else:
            mic.say('窗帘君暂无法理解你的指令哦')
        curtain_device.send_desire_stat_to_iotx(device=curtain.DEVICE_NAME, cmd=cmd)       # 发送设备的动作到IoTHub

    if is_all_word_segment_in_text(['灯'], text):       # 灯控制
        if is_all_word_segment_in_text(['打开'], text):
            mic.say('夜灯已打开')
        elif is_all_word_segment_in_text(['关闭', '关上'], text):
            mic.say('夜灯已关闭')


def is_valid(text):
    return is_all_word_segment_in_text(WORDS, text)

