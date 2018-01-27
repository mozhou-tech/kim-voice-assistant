# -*- coding: utf-8-*-
import logging
from src.plugins import is_all_word_segment_in_text

WORDS = [u"echo", u"用英文"]
PRIORITY = 0


def handle(text, mic, profile, iot_client=None,chatbot=None):
    """
        Reports the current time based on the user's timezone.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    logger = logging.getLogger()
    text = text.replace('echo', '').replace(u'传话', '')
    mic.say(text)


def is_valid(text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return is_all_word_segment_in_text(WORDS, text)
