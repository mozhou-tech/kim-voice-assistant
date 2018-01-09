# -*- coding: utf-8-*-
import logging
import requests
import json

WORDS = [u"天气"]
PRIORITY = 0
logger = logging.getLogger()
from utils.aliyun_fc.fc_client import FcClient


def handle(text, mic):
    """
        Reports the current time based on the user's timezone.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    fc_client = FcClient.get_instance()
    data = {
        'host': 'http://freecityid.market.alicloudapi.com',
        'path': '/whapi/json/alicityweather/briefforecast3days',
        'method': 'POST',
        'appcode': 'cd08e261838a42328340f49cd28c02b4',
        'payload': {
            'cityId': '1045'
        },
        'bodys': {},
        'querys': ''
    }
    result = fc_client.call_function('aliyun_apimarket', payload=data)
    mic.say(result.data.decode('utf8'))


def isValid(text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return any(word in text.lower() for word in WORDS)

