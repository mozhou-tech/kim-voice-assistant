# -*- coding: utf-8-*-
import random
# from client.robot import get_robot_by_slug

WORDS = []
PRIORITY = -99999


def handle(text, mic, profile, iot_client=None):

    messages = [u"抱歉，您能再说一遍吗？",
                u"听不清楚呢，可以再为我说一次吗？",
                u"再说一遍好吗？"]
    message = random.choice(messages)
    mic.say(message)


def is_valid(text):
    return True
