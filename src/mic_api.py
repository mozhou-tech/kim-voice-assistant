# -*- coding: utf-8-*-
import logging

class Mic:
    def __init__(self, speaker, passive_stt_engine, active_stt_engine):
        self.speaker = speaker

    def passiveListen(self, PERSONA):
        return True, "DINGDANG"

    def activeListenToAllOptions(self, THRESHOLD=None, LISTEN=True,
                                 MUSIC=False):
        return [self.activeListen(THRESHOLD=THRESHOLD, LISTEN=LISTEN,
                                  MUSIC=MUSIC)]

    def activeListen(self, THRESHOLD=None, LISTEN=True, MUSIC=False):
        if not LISTEN:
            return self.prev

        input_content = input("YOU: ")
        self.prev = input_content
        return input_content

    def say(self, phrase):
        """
        输出内容
        :param phrase:
        :return:
        """
        print("DINGDANG: %s" % phrase)
        self.speaker.say()

    def play(self, src):
        # play a voice
        self.speaker.play(src)





