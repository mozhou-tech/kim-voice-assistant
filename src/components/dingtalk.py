#!/usr/bin/python
# coding=utf-8
import requests
import json,logging
import sys
import socket
# -*- coding: utf-8-*-
from src import config


class DingRobot:
    def __init__(self):
        self.yaml_settings = config.load_yaml_settings()

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
        print(response_json)
        if response_json['errcode'] != 0:
            logger.info('dingtalk 发送消息错误：%s', response_json['errmsg'])
            return False
        else:
            return True





