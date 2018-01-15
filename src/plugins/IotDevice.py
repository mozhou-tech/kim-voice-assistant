# -*- coding: utf-8-*-
import logging
import requests
import json
import random,math

WORDS = ["把灯打开", '打开窗帘']
PRIORITY = 0
logger = logging.getLogger()
from utils.aliyun_fc.fc_client import FcClient
from config.path import APP_PATH
from src.plugins import is_all_word_segment_in_text


def handle(text, mic, profile):
    pass


def is_valid(text):
    return is_all_word_segment_in_text(WORDS, text)

