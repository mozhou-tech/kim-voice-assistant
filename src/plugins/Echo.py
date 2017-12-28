# -*- coding: utf-8-*-
import logging

WORDS = [u"ECHO", u"传话"]
SLUG = "echo"
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
    logger.info("使用%s插件处理", SLUG)
    text = text.lower().replace('echo', '').replace(u'传话', '')
    mic.say(text)


def isValid(text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return any(word in text.lower() for word in WORDS)
