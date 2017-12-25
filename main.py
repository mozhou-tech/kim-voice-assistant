#!/usr/bin/env python2
# -*- coding: utf-8-*-

import os
import sys
import logging
import time
import yaml
import argparse
import threading
from client import tts, config
from client import stt
from client import diagnose
from client.conversation import Conversation
from utils import WechatBot
from client.audio_utils import mp3_to_wav



# Add xiaoyunpath.LIB_PATH to sys.path
sys.path.append(config.LIB_PATH)

parser = argparse.ArgumentParser(description='xiaoyun Voice Control Center')
parser.add_argument('--local', action='store_true',
                    help='Use text input instead of a real microphone')
parser.add_argument('--no-network-check', action='store_true',
                    help='Disable the network connection check')
parser.add_argument('--diagnose', action='store_true',
                    help='Run diagnose and exit')
parser.add_argument('--debug', action='store_true', help='Show debug messages')
parser.add_argument('--info', action='store_true', help='Show info messages')
args = parser.parse_args()

if args.local:
    from client.local_mic import Mic
else:
    from client.mic import Mic


class xiaoyun(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)

        # Create config dir if it does not exist yet
        if not os.path.exists(config.CONFIG_PATH):
            try:
                os.makedirs(config.CONFIG_PATH)
            except OSError:
                self._logger.error("Could not create config dir: '%s'",
                                   config.CONFIG_PATH, exc_info=True)
                raise

        # Check if config dir is writable
        if not os.access(config.CONFIG_PATH, os.W_OK):
            self._logger.critical("Config dir %s is not writable. xiaoyun " +
                                  "won't work correctly.",
                                  config.CONFIG_PATH)

        config_file = config.config('profile.yml')
        # Read config
        self._logger.debug("Trying to read config file: '%s'", config_file)
        try:
            with open(config_file, "r") as f:
                self.config = yaml.safe_load(f)
        except OSError:
            self._logger.error("Can't open config file: '%s'", config_file)
            raise

        try:
            stt_engine_slug = self.config['stt_engine']
        except KeyError:
            stt_engine_slug = 'sphinx'
            logger.warning("stt_engine not specified in profile, defaulting " +
                           "to '%s'", stt_engine_slug)
        stt_engine_class = stt.get_engine_by_slug(stt_engine_slug)

        try:
            slug = self.config['stt_passive_engine']
            stt_passive_engine_class = stt.get_engine_by_slug(slug)
        except KeyError:
            stt_passive_engine_class = stt_engine_class

        try:
            tts_engine_slug = self.config['tts_engine']
        except KeyError:
            tts_engine_slug = tts.get_default_engine_slug()
            logger.warning("tts_engine not specified in profile, defaulting " +
                           "to '%s'", tts_engine_slug)
        tts_engine_class = tts.get_engine_by_slug(tts_engine_slug)

        # Initialize Mic
        self.mic = Mic(
            self.config,
            tts_engine_class.get_instance(),
            stt_passive_engine_class.get_passive_instance(),
            stt_engine_class.get_active_instance())

    def start_wxbot(self):
        print("请扫描如下二维码登录微信")
        print("登录成功后，可以与自己的微信账号（不是文件传输助手）交互")
        self.wxBot.run(self.mic)

    def run(self):
        if 'first_name' in self.config:
            salutation = (u"%s 我能为您做什么?"
                          % self.config["first_name"])
        else:
            salutation = "主人，我能为您做什么?"

        persona = 'xiaoyun'
        if 'robot_name' in self.config:
            persona = self.config["robot_name"]
        conversation = Conversation(persona, self.mic, self.config)

        # create wechat robot
        if self.config['wechat']:
            self.wxBot = WechatBot(conversation.brain)
            self.wxBot.DEBUG = True
            self.wxBot.conf['qr'] = 'tty'
            conversation.wxbot = self.wxBot
            t = threading.Thread(target=self.start_wxbot)
            t.start()

        self.mic.say(salutation)
        conversation.handleForever()


if __name__ == "__main__":

    logging.basicConfig(
        filename=os.path.join(
            config.LOG_PATH, "xiaoyun.log"
        ),
        filemode="w",
        format='%(asctime)s %(filename)s[line:%(lineno)d] \
        %(levelname)s %(message)s',
        level=logging.INFO)
    logger = logging.getLogger()
    logger.getChild("client.stt").setLevel(logging.INFO)

    if args.debug:
        logger.setLevel(logging.DEBUG)
    elif args.info:
        logger.setLevel(logging.INFO)

    if not args.no_network_check and not diagnose.check_network_connection():
        logger.warning("Network not connected. This may prevent xiaoyun " +
                       "from running properly.")

    if args.diagnose:
        failed_checks = diagnose.run()
        sys.exit(0 if not failed_checks else 1)

    app = xiaoyun()
    app.run()
