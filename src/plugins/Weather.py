# -*- coding: utf-8-*-
import logging
import requests

WORDS = [u"天气"]
PRIORITY = 0
logger = logging.getLogger()


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
    path = '/whapi/json/alicityweather/briefforecast3days'
    method = 'POST'
    appcode = 'cd08e261838a42328340f49cd28c02b4'
    querys = ''
    bodys = {}
    url = host + path

    payload = {
        'cityId': '''2''',
        'token': '''677282c2f1b3d718152c4e25ed434bc4'''
    }
    headers = {
      'Authorization': 'APPCODE ' + appcode,
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    r = requests.request(method=method, url=url, data=payload, headers=headers)
    logger.info('request api %s', r.url)
    print(r.text)
