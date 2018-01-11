#!/usr/bin/python
# coding=utf-8
import urllib
import urllib2
import json
import sys
import socket



# 获取钉钉消息
def extractionMessage():
    # 拼接需要发送的消息
    return "##### <font color=orange> 钉钉message </font>"


# 发送钉钉消息
def sendDingDingMessage(url, data):
    req = urllib2.Request(url)
    req.add_header("Content-Type", "application/json; charset=utf-8")
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(req, json.dumps(data))
    return response.read()


# 主函数
def main():
    posturl = "https://oapi.dingtalk.com/robot/send?access_token=????????????????????????????"
    data = {"msgtype": "markdown", "markdown": {"text": extractionMessage(), "title": "Jenkins", "isAtAll": "false"}}
    sendDingDingMessage(posturl, data)


main()