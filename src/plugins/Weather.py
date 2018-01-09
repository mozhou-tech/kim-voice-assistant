# -*- coding: utf-8-*-
import logging
import requests
import json

WORDS = [u"天气"]
PRIORITY = 0
logger = logging.getLogger()
from utils.aliyun_fc.fc_client import FcClient
import xml.etree.ElementTree as ET
from config.profile import city
from config.path import APP_PATH


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

    tree = ET.parse(APP_PATH + '/src/plugins/resources/weather-moji-citys.xml')  # 载入数据
    xml_root = tree.getroot()    #获取根节点
    elements = xml_root.findall('./city[@name="' + city + '"]')
    if elements is None:
        mic.say('没有找到你设定的城市，请修改profile配置文件')
        return
    else:
        city_id = elements[0].get('id')
    data = {
        'host': 'http://freecityid.market.alicloudapi.com',
        'path': '/whapi/json/alicityweather/briefforecast3days',
        'method': 'POST',
        'appcode': 'cd08e261838a42328340f49cd28c02b4',
        'payload': {
            'cityId': city_id
        },
        'bodys': {},
        'querys': ''
    }
    return_text = ''
    result_raw = json.loads(fc_client.call_function('aliyun_apimarket', payload=data).data.decode('utf8'))
    if result_raw['msg'] == 'success':
        return_text += '为您播报'+result_raw['data']['city']['name']+'天气，'
        today = result_raw['data']['forecast'][0]
        tomorrow = result_raw['data']['forecast'][1]
        return_text += '今天'+today['conditionDay']+'，白天气温，'+today['tempDay'].replace('-', '零下')+\
                       '摄氏度，夜间气温，'+today['tempNight'].replace('-', '零下')+\
                       '摄氏度，'+today['windDirNight']+today['windLevelDay'].replace('-', '到')+'级'
        return_text += '，，明天'+tomorrow['conditionDay']+'，白天气温'+tomorrow['tempDay'].replace('-', '零下')+\
                       '摄氏度，夜间气温，'+tomorrow['tempNight'].replace('-', '零下')+'摄氏度，'+\
                       tomorrow['windDirNight']+tomorrow['windLevelDay'].replace('-', '到')+'级'
    mic.say(return_text)


def isValid(text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return any(word in text.lower() for word in WORDS)

