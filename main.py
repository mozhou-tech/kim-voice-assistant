#!/usr/bin/env
# -*- coding: utf-8-*-


from src.detector import Detector

from utils.logger import init as loggingConfiger
import logging
from src.conversation import Conversation
from config import profile
import argparse


parser = argparse.ArgumentParser(description='')
parser.add_argument('--textmode', action='store_true', help='使用文本交互')
parser.add_argument('--diagnose', action='store_true', help='Run diagnose and exit')
# 调试模式
parser.add_argument('--debug', action='store_true', help='Show debug messages')
parser.add_argument('--info', action='store_true', help='Show info messages')
args = parser.parse_args()
if args.textmode:
    from src.mic_text import Mic
else:
    from src.mic_voice import Mic


class App:
    def __init__(self):
        self.persona = 'abc'
        # Initialize Mic
        self.mic = Mic()

    def run(self):
        conversation = Conversation(mic=self.mic, persona=self.persona, profile=profile)
        conversation.handle_forever()


if __name__ == "__main__":
    loggingConfiger(info=args.info, debug=args.debug)      # 配置logging
    logger = logging.getLogger()
    app = App()
    app.run()  # start service


