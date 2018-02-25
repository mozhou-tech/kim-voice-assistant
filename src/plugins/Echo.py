# -*- coding: utf-8-*-
import logging

WORDS = ["echo", "传话", "重复一下"]
PRIORITY = 0
logger = logging.getLogger()
from src.plugins import is_all_word_segment_in_text,plugin_output


def handle(text, mic, profile, iot_client=None,chatbot=None):
    """
        Reports the current time based on the user's timezone.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    text_str = ''.join(text)
    robot_says = text_str.replace('echo', '').replace('传话', '').replace('重复一下', '')
    plugin_output(text, mic, robot_says)


def is_valid(text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return is_all_word_segment_in_text(WORDS, text)
