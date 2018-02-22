#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

from logzero import logger
import zmq
import time
import snowboydecoder
import sys
import signal

interrupted = False

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

def sendMessage(publisher):
  def callback():
    publisher.send_multipart(['hotword', '1'])
    snowboydecoder.play_audio_file()
  return callback

def main(model):
    """ Main entry point of the app """
    logger.info("hello world")
    context = zmq.Context()
    publisher = context.socket (zmq.PUB)
    publisher.bind ("tcp://*:8888")
    detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
    detector.start(detected_callback=sendMessage(publisher),
                  interrupt_check=interrupt_callback,
                  sleep_time=0.03)
    detector.terminate()        

signal.signal(signal.SIGINT, signal_handler)

if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python main.py your.model")
    sys.exit(-1)

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main(sys.argv[1])
