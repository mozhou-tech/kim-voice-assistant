import logging
class Mic:
    def __init__(self, config, speaker, passive_stt_engine, active_stt_engine):
        self.stop_passive = False
        self.skip_passive = False
        self.chatting_mode = False
        return

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




