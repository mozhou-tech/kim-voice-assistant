# -*- coding: utf-8-*-
import logging
from config import profile


class Mic:
    """
    处理文本输出和输入
    """
    def __init__(self):
        pass

    def passive_listen(self):
        """
        被动监听
        :return:
        """
        return True, profile.myname

    def active_listen(self):
        """
        主动监听
        :return:
        """
        input_content = input("我: ")
        return input_content

    def say(self, phrase):
        """
        输出内容
        :param phrase:
        :return:
        """
        print("小云: " + phrase)


