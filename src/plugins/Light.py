# -*- coding: utf-8-*-
import logging
import requests
import json
from gpiozero import RGBLED
from time import sleep

WORDS = ["开灯", "把灯打开"]
PRIORITY = 0
logger = logging.getLogger()
from utils.aliyun_fc.fc_client import FcClient
import xml.etree.ElementTree as ET
from config.profile import city, myname, ali_appcode
from config.path import APP_PATH
from src.plugins import is_all_word_segment_in_text


def handle(text, mic, profile):
    led = RGBLED(red=9, green=10, blue=11)
    led.color = (0, 0, 0)  # 白色，搞一个转换函数，把高低电平变成255,255,255,255


    while True:
        led.red = 1  # full red
        sleep(1)
        led.red = 0.5  # half red
        sleep(1)

        led.color = (0, 1, 0)  # full green
        sleep(1)
        led.color = (1, 0, 1)  # magenta
        sleep(1)
        led.color = (1, 1, 0)  # yellow
        sleep(1)
        led.color = (0, 1, 1)  # cyan
        sleep(1)
        led.color = (1, 1, 1)  # white
        sleep(1)

        led.color = (0, 0, 0)  # off

        sleep(1)
    mic.say('天气获取失败')


def is_valid(text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return is_all_word_segment_in_text(WORDS, text)

