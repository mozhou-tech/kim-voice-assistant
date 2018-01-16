# -*- coding: utf-8-*-
import random
# from client.robot import get_robot_by_slug

WORDS = []
PRIORITY = -99999


def handle(text, mic, profile, iot_client=None):
    """
    内部实现完整的对话逻辑，对原来的逻辑无侵入
    :param text:
    :param mic:
    :param profile:
    :return:
    """
    # 进入循环
    # 退出循环
    mic.say('')


def is_valid(text):
    return True
