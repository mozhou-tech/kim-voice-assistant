from src.brain import Brain
import logging, time


class Conversation:
    """
    交谈
    """
    def __init__(self, mic, persona, profile):
        self._logger = logging.getLogger()
        self.text_mode = False
        self.mic = mic
        self.profile = profile
        self.persona = persona
        self._logger.debug(mic)
        self.brain = Brain(mic, profile)

    def is_proper_time(self):
        """
        是否是适当的交谈时间
        :return:
        """
        return True

    def handle_forever(self):
        """
        持续处理
        :return:
        """
        while True:
            self._logger.info('handle an item of conversation.')

            if self.mic.stop_passive:  # 主动模式
                self._logger.info("skip conversation for now.")
                time.sleep(1)
                continue
            if not self.mic.skip_passive:  # 主动模式
                threshold, transcribed = self.mic.passiveListen(self.persona)
            else:
                self._logger.debug("Skip passive listening")
                if not self.mic.chatting_mode:
                    self.mic.skip_passive = False
            input_content = self.mic.activeListenToAllOptions(threshold)
            if input_content:
                self.brain.query(input_content)
            else:
                self.mic.say("什么?")








