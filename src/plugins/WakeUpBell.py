# -*- coding: utf-8-*-
import random
import jieba, logging
# from client.robot import get_robot_by_slug

WORDS = ["叫我起床", "过几分钟再叫我"]
cut_words = []
PRIORITY = 6
logger = logging.getLogger(__name__)

def need_robot(profile):
    if 'robot' in profile and profile['robot'] is not None:
        return True
    return False


def handle(text, mic, profile):
    """
    Reports that the user has unclear or unusable input.

    Arguments:
    text -- user-input, typically transcribed speech
    mic -- used to interact with the user (for both input and output)
    profile -- contains information related to the user (e.g., phone
               number)
    wxBot -- wechat robot
    """
    message = "起床铃响了"
    mic.say(message)
    logger.info(any(word in text for word in WORDS))


def isValid(text):
    for word in WORDS:
        cut_words.append(list(jieba.cut(word)))
    print(cut_words)
    return any(word in text for word in WORDS)
