# -*- coding: utf-8-*-
import random
import jieba, logging
# from client.robot import get_robot_by_slug
from src.plugins import is_all_word_segment_in_text

WORDS = ["闹铃", "叫我起床"]
PRIORITY = 6
logger = logging.getLogger()


def handle(text, mic, profile, iot_client=None,chatbot=None):
    message = "嗨，伙计，该起床了！"
    mic.say(message)


def is_valid(text):
    return is_all_word_segment_in_text(WORDS, text)


