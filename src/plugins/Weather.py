# -*- coding: utf-8-*-
import logging
import requests
import json

WORDS = [u"天气"]
PRIORITY = 0
logger = logging.getLogger()
from utils.aliyun_fc.fc_client import FcClient
import xml.etree.ElementTree as ET
from config.profile import city, myname
from config.path import APP_PATH
from src.plugins import is_all_word_segment_in_text


def handle(text, mic, profile):
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
    try:
        city_id = elements[0].get('id')
    except:
        mic.say('没有找到你设定的城市，请修改profile配置文件')
    finally:
        if city_id is None:
            mic.say('没有找到你设定的城市，请修改profile配置文件')


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
        return_text += myname+'为您播报，'+result_raw['data']['city']['name']+'天气预报，'
        if is_all_word_segment_in_text(['明天'], text):
            forecast = result_raw['data']['forecast'][1]
            day = '明天'
        elif is_all_word_segment_in_text(['后天'], text):
            forecast = result_raw['data']['forecast'][2]
            day = '后天'
        else:
            forecast = result_raw['data']['forecast'][0]
            day = '今天'
        forecast_output = day + forecast['conditionDay']+'，白天气温，'+forecast['tempDay'].replace('-', '零下')+\
                       '摄氏度，夜间气温，'+forecast['tempNight'].replace('-', '零下')+\
                       '摄氏度，'+forecast['windDirNight']+forecast['windLevelDay'].replace('-', '到')+'级'
        mic.say(forecast_output)
    else:
        mic.say('天气获取失败')


def is_valid(text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return is_all_word_segment_in_text(WORDS, text)

