#!/usr/bin/python
# coding=utf-8
import requests
import json,logging
import sys,os
import socket, importlib
from src.config import load_yaml_settings
from src.components.semantic import is_all_word_segment_in_text
logger = logging.getLogger()


class DingRobot:

    def __init__(self):
        self.yaml_settings = load_yaml_settings()

    @classmethod
    def dingtalk_handle(cls, text, robot_says):
        """
        钉钉消息处理
        :param text:
        :param mic:
        :param robot_says:
        :return:
        """
        if is_all_word_segment_in_text(["发送到钉钉", '发到钉钉', '发到丁丁', '发送到丁丁'], text):
            ret = cls.send_message(title=''.join(text), markdown_content=robot_says)
            if ret:
                logger.info('钉钉消息发送成功')
            else:
                logger.error('钉钉消息发送失败')

    def get_token(self):
        return self.yaml_settings['dingding']['robot_token']

    # 发送钉钉消息
    @classmethod
    def send_message(cls, title, markdown_content=None):
        """
        发送消息
        :param title: 消息标题会单行文本内容
        :param markdown_content: 支持MarkDown语法
        :return:
        """
        dingding = DingRobot()
        logger = logging.getLogger()
        posturl = "https://oapi.dingtalk.com/robot/send?access_token=" + dingding.get_token()
        if markdown_content is None:
            data = {
                "msgtype": "text",
                "text": {
                    "content": title
                }
            }
        else:

            data = {
                 "msgtype": "markdown",
                 "markdown": {
                     "title": title,
                     "text": markdown_content
                 }
            }

        response = requests.post(url=posturl, data=json.dumps(data), headers={
            "Content-Type": "application/json",
            "charset": "utf-8"
        })
        response_json = json.loads(response.content.decode('utf8'))
        if response_json['errcode'] != 0:
            logger.info('dingtalk 发送消息错误：%s', response_json['errmsg'])
            return False
        else:
            return True





