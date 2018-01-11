# -*- coding: utf-8-*-
import logging

WORDS = [u"echo", u"传话"]
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
    logger = logging.getLogger(__name__)
    text = text.lower().replace('echo', '').replace(u'传话', '')
    mic.say(text)


def is_valid(text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return any(word in text.lower() for word in WORDS)
