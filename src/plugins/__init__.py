# -*- coding: utf-8-*-

import jieba, logging
from src.components.dingtalk import DingRobot
logger = logging.getLogger()

from src.components.semantic import is_all_word_segment_in_text


def plugin_output(text, mic, robot_says):
    """
    插件输出
    :param text:
    :param mic:
    :param robot_says:
    :return:
    """
    DingRobot.dingtalk_handle(text, robot_says)
    mic.say(robot_says)
