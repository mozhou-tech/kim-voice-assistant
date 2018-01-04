# -*- coding: utf-8 -*-
import logging
import requests
import json
import asr
import tts

def my_handler(event, context):

  params = json.loads(event)
  url = params['host'] + params['path']
  headers = {
    'Authorization': 'APPCODE ' + params['appcode'],
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
  }
  r = requests.request(method=params['method'], url=url, data=params['payload'], headers=headers)
  return r.text