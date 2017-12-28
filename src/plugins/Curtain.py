# -*- coding: utf-8-*-
import logging

WORDS = [u"窗帘"]
PRIORITY = 0


def handle(text, mic, profile):
    """
        Reports the current time based on the user's timezone.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    logger = logging.getLogger()
    if any(word in text.lower() for word in [u"打开"]):
        text = u"窗帘已打开"
    elif any(word in text.lower() for word in [u"关闭"]):
        text = u"窗帘已关闭"
    else:
        text = u"窗帘还不支持该指令"
    mic.say(text)


def isValid(text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return any(word in text.lower() for word in WORDS)
