# -*- coding: utf-8-*-
"""
A Speaker handles audio output from xiaoyun to the user

Speaker methods:
    say - output 'phrase' as speech
    play - play the audio in 'filename'
    is_available - returns True if the platform supports this implementation
"""
import os
import platform
import re
import tempfile
import subprocess
import pipes
import logging
import urllib
import urllib.parse
import requests
import datetime
import base64
import hmac
import hashlib
from dateutil import parser as dparser
from abc import ABCMeta, abstractmethod
from uuid import getnode as get_mac

import argparse
import yaml

from client import diagnose, config as config_path

try:
    import gtts
except ImportError:
    pass

import sys
import importlib
importlib.reload(sys)


class AbstractTTSEngine(object):
    """
    Generic parent class for all speakers
    """
    __metaclass__ = ABCMeta

    @classmethod
    def get_config(cls):
        return {}

    @classmethod
    def get_instance(cls):
        config = cls.get_config()
        instance = cls(**config)
        return instance

    @classmethod
    @abstractmethod
    def is_available(cls):
        return diagnose.check_executable('aplay')

    def __init__(self, **kwargs):
        self._logger = logging.getLogger(__name__)

    @abstractmethod
    def say(self, phrase, *args):
        pass

    def play(self, filename):
        cmd = ['aplay', str(filename)]
        self._logger.debug('Executing %s', ' '.join([pipes.quote(arg)
                                                     for arg in cmd]))
        with tempfile.TemporaryFile() as f:
            subprocess.call(cmd, stdout=f, stderr=f)
            f.seek(0)
            output = f.read()
            if output:
                self._logger.debug("Output was: '%s'", output)


class AbstractMp3TTSEngine(AbstractTTSEngine):
    """
    Generic class that implements the 'play' method for mp3 files
    """
    SLUG = ''

    @classmethod
    def is_available(cls):
        return (super(AbstractMp3TTSEngine, cls).is_available() and
                diagnose.check_python_import('mad'))

    def play_mp3(self, filename, remove=False):
        cmd = [u'play', str(filename)]
        self._logger.debug('Executing %s', ' '.join([pipes.quote(arg)
                                                     for arg in cmd]))
        with tempfile.TemporaryFile() as f:
            p = subprocess.Popen(cmd, stdout=f, stderr=f)
            p.wait()
            f.seek(0)
            output = f.read()
            if output:
                self._logger.debug("Output was: '%s'", output)

    @abstractmethod
    def get_speech(self, phrase):
        pass

    def say(self, phrase, cache=False):
        self._logger.debug(u"Saying '%s' with '%s'", phrase, self.SLUG)
        cache_file_path = config_path.data(
            'audio',
            self.SLUG + phrase + '.mp3'
        )
        if cache and os.path.exists(cache_file_path):
            self._logger.info(
                "found speech in cache, playing...[%s]" % cache_file_path)
            self.play_mp3(cache_file_path)
        else:
            tmpfile = self.get_speech(phrase)
            if tmpfile is not None:
                self.play_mp3(tmpfile)
                if cache:
                    self._logger.info(
                        "not found speech in cache," +
                        " caching...[%s]" % cache_file_path)
                    os.rename(tmpfile, cache_file_path)
                else:
                    os.remove(tmpfile)


class SimpleMp3Player(AbstractMp3TTSEngine):
    """
    MP3 player for playing mp3 files
    """
    SLUG = "mp3-player"

    @classmethod
    def is_available(cls):
        return True

    def say(self, phrase):
        self._logger.info(phrase)


class MacOSXTTS(AbstractTTSEngine):
    """
    Uses the OS X built-in 'say' command
    """

    SLUG = "osx-tts"

    @classmethod
    def is_available(cls):
        return (platform.system().lower() == 'darwin' and
                diagnose.check_executable('say') and
                diagnose.check_executable('afplay'))

    def say(self, phrase):
        self._logger.debug("Saying '%s' with '%s'", phrase, self.SLUG)
        cmd = ['say', str(phrase)]
        self._logger.debug('Executing %s', ' '.join([pipes.quote(arg)
                                                     for arg in cmd]))
        with tempfile.TemporaryFile() as f:
            subprocess.call(cmd, stdout=f, stderr=f)
            f.seek(0)
            output = f.read()
            if output:
                self._logger.debug("Output was: '%s'", output)

    def play(self, filename):
        cmd = ['aplay', str(filename)]
        self._logger.debug('Executing %s', ' '.join([pipes.quote(arg)
                                                     for arg in cmd]))
        with tempfile.TemporaryFile() as f:
            subprocess.call(cmd, stdout=f, stderr=f)
            f.seek(0)
            output = f.read()
            if output:
                self._logger.debug("Output was: '%s'", output)


class ALiBaBaTTS(AbstractMp3TTSEngine):
    """
    使用阿里云的语音合成技术
    要使用本模块, 请先在 profile.xml 中启用本模块并选择合适的发音人.
    """

    SLUG = "ali-tts"

    def __init__(self, ak_id, ak_secret, voice_name='xiaoyun'):
        self._logger = logging.getLogger(__name__)
        self.ak_id = ak_id
        self.ak_secret = ak_secret
        self.voice_name = voice_name

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
                    if 'voice_name' in profile['ali_yuyin']:
                        config['voice_name'] = \
                            profile['ali_yuyin']['voice_name']
        return config

    @classmethod
    def is_available(cls):
        return diagnose.check_network_connection()

    def split_sentences(self, text):
        punctuations = ['.', '。', ';', '；', '\n']
        for i in punctuations:
            text = text.replace(i, '@@@')
        return text.split('@@@')

    def get_current_date(self):
        date = datetime.datetime.strftime(datetime.datetime.utcnow(),
                                          "%a, %d %b %Y %H: %M: %S GMT")
        return date

    def to_md5_base64(self, strBody):
        hash = hashlib.md5()
        hash.update(strBody)
        return base64.b64encode(hash.digest()).strip()

    def to_sha1_base64(self, stringToSign, secret):
        stringToSign = bytes(stringToSign, 'utf-8')
        secret = bytes(secret, 'utf-8')
        hmacsha1 = hmac.new(secret, stringToSign, hashlib.sha1)
        return base64.b64encode(hmacsha1.digest())

    def get_speech(self, phrase):
        options = {
            'url': 'http://nlsapi.aliyun.com/speak?encode_type=' +
            'mp3&voice_name=' + self.voice_name + '&volume=50',
            'method': 'POST',
            'body': phrase.encode('utf8'),
        }
        headers = {
            'date': self.get_current_date(),
            'content-type': 'text/plain',
            'authorization': '',
            'accept': 'audio/wav, application/json'
        }

        body = ''
        if 'body' in options:
            body = options['body']

        bodymd5 = ''
        if not body == '':
            bodymd5 = self.to_md5_base64(body)

        stringToSign = options['method'] + '\n' + headers['accept'] + '\n' + \
            str(bodymd5, 'utf-8') + '\n' + headers['content-type'] + '\n' + headers['date']
        signature = self.to_sha1_base64(stringToSign, self.ak_secret)
        authHeader = 'Dataplus ' + str(self.ak_id) + ':' + str(signature)
        headers['authorization'] = authHeader
        url = options['url']
        r = requests.post(url, data=body, headers=headers, verify=False)
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            f.write(r.content)
            tmpfile = f.name
            return tmpfile


def get_default_engine_slug():
    return 'osx-tts' if platform.system().lower() == 'darwin' else 'espeak-tts'


def get_engine_by_slug(slug=None):
    """
    Returns:
        A speaker implementation available on the current platform

    Raises:
        ValueError if no speaker implementation is supported on this platform
    """

    if not slug or type(slug) is not str:
        raise TypeError("Invalid slug '%s'", slug)

    selected_engines = list(filter(lambda engine: hasattr(engine, "SLUG") and
                              engine.SLUG == slug, get_engines()))
    if len(selected_engines) == 0:
        raise ValueError("No TTS engine found for slug '%s'" % slug)
    else:
        if len(selected_engines) > 1:
            print("WARNING: Multiple TTS engines found for slug '%s'. " +
                  "This is most certainly a bug." % slug)
        engine = selected_engines[0]
        if not engine.is_available():
            raise ValueError(("TTS engine '%s' is not available (due to " +
                              "missing dependencies, etc.)") % slug)
        return engine


def get_engines():
    def get_subclasses(cls):
        subclasses = set()
        for subclass in cls.__subclasses__():
            subclasses.add(subclass)
            subclasses.update(get_subclasses(subclass))
        return subclasses
    return [tts_engine for tts_engine in
            list(get_subclasses(AbstractTTSEngine))
            if hasattr(tts_engine, 'SLUG') and tts_engine.SLUG]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='xiaoyun TTS module')
    parser.add_argument('--debug', action='store_true',
                        help='Show debug messages')
    args = parser.parse_args()

    logging.basicConfig()
    if args.debug:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

    engines = get_engines()
    available_engines = []
    for engine in get_engines():
        if engine.is_available():
            available_engines.append(engine)
    disabled_engines = list(set(engines).difference(set(available_engines)))
    print("Available TTS engines:")
    for i, engine in enumerate(available_engines, start=1):
        print("%d. %s" % (i, engine.SLUG))

    print("")
    print("Disabled TTS engines:")

    for i, engine in enumerate(disabled_engines, start=1):
        print("%d. %s" % (i, engine.SLUG))

    print("")
    for i, engine in enumerate(available_engines, start=1):
        print("%d. Testing engine '%s'..." % (i, engine.SLUG))
        engine.get_instance().say("This is a test.")
    print("Done.")
