# -*- coding: utf-8-*-
import logging

class Mic:
    def __init__(self):
        return

    def passiveListen(self, persona):
        return True, persona

    def activeListen(self, THRESHOLD=None, LISTEN=True, MUSIC=False):
        if not LISTEN:
            return self.prev

        input_content = input(u"我: ")
        self.prev = input_content
        return input_content

    def activeListenToAllOptions(self, THRESHOLD=None, LISTEN=True,
                                 MUSIC=False):
        return [self.activeListen(THRESHOLD=THRESHOLD, LISTEN=LISTEN,
                                  MUSIC=MUSIC)]

    def say(self, phrase):
        """
        输出内容
        :param phrase:
        :return:
        """
        print(u"小云: %s" % phrase)


