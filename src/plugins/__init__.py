# -*- coding: utf-8-*-

import jieba, logging
from src.components.dingtalk import DingRobot
from src.config import load_yaml_settings
from src.components.semantic import is_all_word_segment_in_text
logger = logging.getLogger()


def plugin_output(text, mic, robot_says, force_ding=False, ding_content=None):
    """
    插件输出
    :param text:
    :param mic:
    :param robot_says:
    :param force_ding: 此参数为True时，返回消息肯定会发送到钉钉
    :param ding_content: 钉钉消息内容
    :return:
    """
    ding_says = robot_says
    if load_yaml_settings()['dingtalk']['enable'] or force_ding:
        if ding_content is not None:
            ding_says = ding_content
        DingRobot.dingtalk_handle(text, ding_says, force_ding)
    mic.say(robot_says)
