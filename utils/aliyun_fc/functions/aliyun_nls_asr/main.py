# -*- coding: utf-8 -*-
import httplib, urllib, md5
from hashlib import sha1
import hmac
from time import gmtime, strftime
import json


def my_handler(event, context):
    """
    入口函数
    :param event:
    :param context:
    :return:
    """
    with open("appsecret.json", 'r') as f:    # 从json中读取ak信息
        appsecret = json.loads(f.read())

    ac_id = appsecret['ak_id']
    ac_secret = appsecret['ak_secret']
    app_key = 'chat'
    method = 'POST'
    accept = 'application/json'
    # accept='text/plain' # tts request

    contentType = 'audio/pcm; samplerate=16000'
    # contentType='audio/opu'
    gmtTime = strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime())

    body = event

    # params = urllib.urlencode({"app_key":app_key, "user_id":aliyun_pk, "vocabulary_id":"en-us"})

    m = md5.new()
    m.update(body)
    m = m.digest()
    bodyhash = m.encode('base64').strip()
    print('body hash: ' + bodyhash)

    m = md5.new()
    m.update(bodyhash)
    m = m.digest()
    finalhash = m.encode('base64').strip()
    print('final hash: ' + finalhash)

    stringToSign = method + '\n' + accept + '\n' + finalhash + '\n' + contentType + '\n' + gmtTime
    signature = hmac.new(str(ac_secret), str(stringToSign), sha1).digest().encode('base64').strip()
    print('signature: ' + signature)
    authHeader = 'Dataplus ' + ac_id + ':' + signature
    print('authHeader: ' + authHeader)

    headers = {"Content-type": contentType, "Accept": accept, "Authorization": authHeader, "Date": gmtTime}

    conn = httplib.HTTPConnection("nlsapi.aliyun.com", 443)
    conn.request("POST", "/recognize?model=" + app_key, body, headers=headers)

    response = conn.getresponse()
    print("response status and reason")
    print(response.status, response.reason)
    print("status done")

    body = response.read()
    print("asr body")
    print(body)
    print("body done")
    conn.close()
    return body

