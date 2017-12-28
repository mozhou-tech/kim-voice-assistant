# -*- coding: utf-8-*-
import logging
import requests
from urllib import parse,request

WORDS = [u"天气"]
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
    text = _fetch_weather_data()
    # if any(word in text.lower() for word in [u"今日", u'今天']):
    #     text = u"窗帘已打开"
    # elif any(word in text.lower() for word in [u"明日", u"明天"]):
    #     text = u"窗帘已关闭"
    # else:
    #     text = u"窗帘还不支持该指令"
    mic.say(text)


def isValid(text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return any(word in text.lower() for word in WORDS)


def _fetch_weather_data():
    host = 'http://freecityid.market.alicloudapi.com'
    path = '/whapi/json/alicityweather/briefcondition'
    method = 'POST'
    appcode = 'cd08e261838a42328340f49cd28c02b4'
    querys = ''
    bodys = {}
    url = host + path

    bodys['cityId'] = '''2'''
    bodys['token'] = '''46e13b7aab9bb77ee3358c3b672a2ae4'''
    post_data = parse.urlencode(bodys)
    request_obj = request.Request(url, post_data)
    request_obj.add_header('Authorization', 'APPCODE ' + appcode)
    # 根据API的要求，定义相对应的Content - Type
    request_obj.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    response = request.urlopen(request_obj)
    return response.read()
