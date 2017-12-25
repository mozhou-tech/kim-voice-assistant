#!/usr/bin/env python2
# -*- coding: utf-8-*-
import os
import base64
import wave
import json
from urllib.parse import urlparse
import tempfile
import logging
import urllib
from abc import ABCMeta, abstractmethod
import requests
import yaml
from client import diagnose, vocabcompiler, config as config_path
from uuid import getnode as get_mac
import hashlib
import datetime
import hmac
import sys
from dateutil import parser as dparser

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class AbstractSTTEngine(object):
    """
    Generic parent class for all STT engines
    """

    __metaclass__ = ABCMeta
    VOCABULARY_TYPE = None

    @classmethod
    def get_config(cls):
        return {}

    @classmethod
    def get_instance(cls, vocabulary_name, phrases):
        config = cls.get_config()
        if cls.VOCABULARY_TYPE:
            vocabulary = cls.VOCABULARY_TYPE(vocabulary_name,
                                             path=config_path.config(
                                                 'vocabularies'))
            if not vocabulary.matches_phrases(phrases):
                vocabulary.compile(phrases)
            config['vocabulary'] = vocabulary
        instance = cls(**config)
        return instance

    @classmethod
    def get_passive_instance(cls):
        phrases = vocabcompiler.get_keyword_phrases()
        return cls.get_instance('keyword', phrases)

    @classmethod
    def get_active_instance(cls):
        phrases = vocabcompiler.get_all_phrases()
        return cls.get_instance('default', phrases)

    @classmethod
    def get_music_instance(cls):
        phrases = vocabcompiler.get_all_phrases()
        return cls.get_instance('music', phrases)

    @classmethod
    @abstractmethod
    def is_available(cls):
        return True

    @abstractmethod
    def transcribe(self, fp):
        pass


class SnowboySTT(AbstractSTTEngine):
    """
    Snowboy STT 离线识别引擎（只适用于离线唤醒）
        ...
        snowboy:
            model: '/home/pi/.xiaoyun/snowboy/xiaoyunxiaoyun.pmdl'  # 唤醒词模型
            sensitivity: "0.5"  # 敏感度
        ...
    """

    SLUG = "snowboy-stt"

    def __init__(self, sensitivity, model, hotword):
        self._logger = logging.getLogger(__name__)
        self.sensitivity = sensitivity
        self.hotword = hotword
        self.model = model
        self.resource_file = os.path.join(config_path.LIB_PATH, 'snowboy/common.res')
        try:
            from snowboy import snowboydetect
        except Exception as e:
            self._logger.critical(e)
            if 'libf77blas.so' in e.message:
                self._logger.critical("您可能需要安装一个so包加载库：" +
                                      "sudo apt-get install libatlas-base-dev")
            return
        self.detector = snowboydetect.SnowboyDetect(
            resource_filename=self.resource_file,
            model_str=self.model)
        self.detector.SetAudioGain(1)
        self.detector.SetSensitivity(self.sensitivity)

    @classmethod
    def get_config(cls):
        # FIXME: Replace this as soon as we have a config module
        config = {}
        # Try to get snowboy config from config
        profile_path = config_path.config('profile.yml')
        if os.path.exists(profile_path):
            with open(profile_path, 'r') as f:
                profile = yaml.safe_load(f)
                if 'snowboy' in profile:
                    if 'model' in profile['snowboy']:
                        config['model'] = \
                            profile['snowboy']['model']
                    else:
                        config['model'] = os.path.join(
                            config_path.LIB_PATH, 'snowboy/xiaoyun.pmdl')
                    if 'sensitivity' in profile['snowboy']:
                        config['sensitivity'] = \
                            profile['snowboy']['sensitivity']
                    else:
                        config['sensitivity'] = "0.5"
                    if 'robot_name' in profile:
                        config['hotword'] = profile['robot_name']
                    else:
                        raise Exception('你需要先帮我取名哦！ 参考文件profile.yml robot_name_cn')
        return config

    def transcribe(self, fp):
        fp.seek(44)
        data = fp.read()
        ans = self.detector.RunDetection(data)
        if ans > 0:
            self._logger.info('snowboy 识别到了: %r', self.hotword)
            return [self.hotword]
        else:
            return []

    @classmethod
    def is_available(cls):
        return diagnose.check_python_import('snowboy.snowboydetect')



class ALiBaBaSTT(AbstractSTTEngine):
    """
    阿里云的语音识别API.
    要使用本模块, 首先到 https://data.aliyun.com/product/nls 注册一个开发者账号,
    然后查看自己的AK信息，填入 profile.xml 中.
    """

    SLUG = "ali-stt"

    def __init__(self, ak_id, ak_secret):
        self._logger = logging.getLogger(__name__)
        self.ak_id = ak_id
        self.ak_secret = ak_secret

    @classmethod
    def get_config(cls):
        # FIXME: Replace this as soon as we have a config module
        config = {}
        # Try to get ali_yuyin config from config
        profile_path = config_path.config('profile.yml')
        if os.path.exists(profile_path):
            with open(profile_path, 'r') as f:
                profile = yaml.safe_load(f)
                if 'ali_yuyin' in profile:
                    if 'ak_id' in profile['ali_yuyin']:
                        config['ak_id'] = \
                            profile['ali_yuyin']['ak_id']
                    if 'ak_secret' in profile['ali_yuyin']:
                        config['ak_secret'] = \
                            profile['ali_yuyin']['ak_secret']
        return config

    def to_md5_base64(self, strBody):
        hash = hashlib.md5()
        hash.update(self.body)
        m = base64.b64encode(hash.digest()).strip()
        hash = hashlib.md5()
        hash.update(m)
        return base64.b64encode(hash.digest()).strip()

    def to_sha1_base64(self, stringToSign, secret):
        stringToSign = bytes(stringToSign,'utf-8')
        secret = bytes(secret,'utf-8')
        hmacsha1 = hmac.new(secret, stringToSign, hashlib.sha1)
        return base64.b64encode(hmacsha1.digest())

    def transcribe(self, fp):
        try:
            wav_file = wave.open(fp, 'rb')
        except IOError:
            self._logger.critical('wav file not found: %s',
                                  fp,
                                  exc_info=True)
            return []
        n_frames = wav_file.getnframes()
        frame_rate = wav_file.getframerate()
        audio = wav_file.readframes(n_frames)
        date = datetime.datetime.strftime(datetime.datetime.utcnow(),
                                          "%a, %d %b %Y %H:%M:%S GMT")
        options = {
            'url': 'https://nlsapi.aliyun.com/recognize?model=chat',
            'method': 'POST',
            'body': audio,
        }
        headers = {
            'authorization': '',
            'content-type': 'audio/wav; samplerate=%s' % str(frame_rate),
            'accept': 'application/json',
            'date': date,
            'Content-Length': str(len(audio))
        }

        self.body = ''
        if 'body' in options:
            self.body = options['body']

        bodymd5 = ''
        if not self.body == '':
            bodymd5 = self.to_md5_base64(self.body)

        stringToSign = options['method'] + '\n' + \
            headers['accept'] + '\n' + str(bodymd5,'utf-8') + '\n' + \
            headers['content-type'] + '\n' + headers['date']
        signature = self.to_sha1_base64(stringToSign, self.ak_secret)

        authHeader = 'Dataplus ' + self.ak_id + ':' + str(signature,'utf-8')
        headers['authorization'] = authHeader
        url = options['url']
        r = requests.post(url, data=self.body, headers=headers, verify=False)
        try:
            text = ''
            if 'result' in r.json():
                text = r.json()['result'].encode('utf-8')
        except requests.exceptions.HTTPError:
            self._logger.critical('Request failed with response: %r',
                                  r.text,
                                  exc_info=True)
            return []
        except requests.exceptions.RequestException:
            self._logger.critical('Request failed.', exc_info=True)
            return []
        except ValueError as e:
            self._logger.critical('Cannot parse response: %s',
                                  e.args[0])
            return []
        except KeyError:
            self._logger.critical('Cannot parse response.',
                                  exc_info=True)
            return []
        else:
            transcribed = []
            if text:
                transcribed.append(text.upper())
            self._logger.info(u'阿里云语音识别到了: %s' % str(text,'utf-8'))
            return transcribed

    @classmethod
    def is_available(cls):
        return diagnose.check_network_connection()



def get_engine_by_slug(slug=None):
    """
    Returns:
        An STT Engine implementation available on the current platform

    Raises:
        ValueError if no speaker implementation is supported on this platform
    """

    if not slug or type(slug) is not str:
        raise TypeError("Invalid slug '%s'", slug)

    selected_engines = list(filter(lambda engine: hasattr(engine, "SLUG") and
                              engine.SLUG == slug, get_engines()))
    if len(selected_engines) == 0:
        raise ValueError("No STT engine found for slug '%s'" % slug)
    else:
        if len(selected_engines) > 1:
            print(("WARNING: Multiple STT engines found for slug '%s'. " +
                   "This is most certainly a bug.") % slug)
        engine = selected_engines[0]
        if not engine.is_available():
            raise ValueError(("STT engine '%s' is not available (due to " +
                              "missing dependencies, missing " +
                              "dependencies, etc.)") % slug)
        return engine


def get_engines():
    def get_subclasses(cls):
        subclasses = set()
        for subclass in cls.__subclasses__():
            subclasses.add(subclass)
            subclasses.update(get_subclasses(subclass))
        return subclasses
    return [tts_engine for tts_engine in
            list(get_subclasses(AbstractSTTEngine))
            if hasattr(tts_engine, 'SLUG') and tts_engine.SLUG]
