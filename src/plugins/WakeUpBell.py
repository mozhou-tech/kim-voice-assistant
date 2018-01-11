# -*- coding: utf-8-*-
import random
import jieba, logging
# from client.robot import get_robot_by_slug
from src.plugins import is_all_word_segment_in_text

WORDS = ["叫我起床", "过几分钟再叫我"]
PRIORITY = 6
logger = logging.getLogger(__name__)


def handle(text, mic, profile):
    message = "起床铃响了"
    mic.say(message)
    logger.info(any(word in text for word in WORDS))


def is_valid(text):
    return is_all_word_segment_in_text(WORDS, text)


