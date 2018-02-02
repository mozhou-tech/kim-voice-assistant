# -*- coding: utf-8-*-

from src.brain import Brain
import logging, time
from utils import logger
# from src.notifier import Notifier


class Conversation:
    """
    交谈
    """
    def __init__(self, mic, persona, profile, iot_client):
        """
        初始化
        :param mic:
        :param persona:
        :param profile:
        :param iot_client:
        :param server_thread: 是否是设备服务线程
        """
        self._logger = logging.getLogger()
        self.text_mode = False
        self.mic = mic
        self.profile = profile
        self.persona = persona
        self._logger.debug(mic)
        self.brain = Brain(mic, profile, iot_client)
        self._is_server_listen_thread = self.mic.is_server_listen_thread
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
        if self._is_server_listen_thread:     # 监听MQTT消息
            def on_message(client, userdata, msg):
                self._logger.info("从服务器监听到MQTT消息： " + msg.topic + " message" + str(msg.payload))
                logger.send_conversation_log(iot_client=self.mic.iot_client, mic='server',
                                             content='我：'+str(msg.payload),
                                             speaker='user')
                if 'mic_text_from_server' in msg.topic:
                    self.send_to_brain(msg.payload.decode('utf8'))  # 订阅到的消息发送到大脑处理
            self._logger.info('进入server listen handle循环')
            self.mic.iot_client.mqttc.on_message = on_message

        else:
            while True:
                # Print notifications until empty  处理邮件等通知
                # notifications = self.notifier.getAllNotifications()
                # for notif in notifications:
                #     self._logger.info("Received notification: '%s'", str(notif))

                self._logger.debug("Started listening for keyword '%s'", self.persona)
                threshold, transcribed = self.mic.passive_listen()
                self._logger.debug("Stopped listening for keyword '%s'", self.persona)

                if not transcribed or not threshold:
                    self._logger.info("Nothing has been said or transcribed.")
                    continue

                self._logger.debug("Started to listen actively with threshold: %r", threshold)
                input_content = self.mic.active_listen()
                self._logger.debug("Stopped to listen actively with threshold: %r", threshold)
                self.send_to_brain(input_content)

    def send_to_brain(self, input_content):
        if input_content:
            self.brain.query(input_content)
        else:
            self.mic.say("你说啥")







