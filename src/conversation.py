from src.brain import Brain
import logging, time
from src.notifier import Notifier


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
        # self.notifier = Notifier(profile)

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
            # Print notifications until empty  处理邮件等通知
            # notifications = self.notifier.getAllNotifications()
            # for notif in notifications:
            #     self._logger.info("Received notification: '%s'", str(notif))

            self._logger.debug("Started listening for keyword '%s'", self.persona)
            threshold, transcribed = self.mic.passiveListen(self.persona)
            self._logger.debug("Stopped listening for keyword '%s'", self.persona)

            if not transcribed or not threshold:
                self._logger.info("Nothing has been said or transcribed.")
                continue
            self._logger.info("Keyword '%s' has been said!", self.persona)

            self._logger.debug("Started to listen actively with threshold: %r", threshold)
            input = self.mic.activeListenToAllOptions(threshold)
            self._logger.debug("Stopped to listen actively with threshold: %r", threshold)
            if input:
                self.brain.query(input)
            else:
                self.mic.say("你说啥?")







