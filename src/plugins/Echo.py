# -*- coding: utf-8-*-
import logging

WORDS = ["echo", "传话", "重复一下"]
PRIORITY = 0
logger = logging.getLogger()
from src.plugins import is_all_word_segment_in_text,plugin_output


def handle(text, mic, profile, iot_client=None, chatbot=None):
    """
    插件处理入口
    :param text: 插件传入文本
    :param mic:
    :param profile:
    :param iot_client: 传入物联网对象，自定插件照写即可
    :param chatbot: 传入chatbot对象
    :return:
    """
    text_str = ''.join(text)
    robot_says = text_str.replace('echo', '').replace('传话', '').replace('重复一下', '')
    plugin_output(text, mic, robot_says,force_ding=True)  # 输出响应


def is_valid(text):
    """
    判断输入text与插件定义的WORDS是否语义匹配
    :param text:
    :return:
    """
    return is_all_word_segment_in_text(WORDS, text)
