# -*- coding: utf-8-*-
import logging

WORDS = [u"播放音乐", u"音乐"]
PRIORITY = 2


def handle(text, mic, profile):
    """
        Reports the current time based on the user's timezone.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    logger = logging.getLogger(__name__)
    text = u"正在播放音乐"
    mic.say(text)


def is_valid(text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return any(word in text.lower() for word in WORDS)
