#!/usr/bin/env
# -*- coding: utf-8-*-


from  src.detector import Detector

from utils import logger
import argparse
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


if __name__ == "__main__":
    logger.init(args)
    detector = Detector()
    detector.main()
