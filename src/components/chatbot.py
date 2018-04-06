# -*- coding: utf-8-*-
from aliyunsdkcore import client
from aliyunsdkchatbot.request.v20171011 import ChatRequest
from src.config import profile
import logging,json
from src.config import load_yaml_settings


class Chatbot:

    def __init__(self):
        """
        初始化
        """
        self.accessKeyId = profile.ak_id
        self.accessKeySecret = profile.ak_secret
        self._logger = logging.getLogger()
        self.chatbot_session_id = None

    def send_message(self, message):
        """
        发送消息到Chatbot
        :param message:
        :return:
        """
        self.clt = client.AcsClient(self.accessKeyId, self.accessKeySecret, load_yaml_settings()['aliyun']['chatbot']['region'])
        self.request = ChatRequest.ChatRequest()
        self.request.set_Utterance(message)
        self.request.set_InstanceId(load_yaml_settings()['aliyun']['chatbot']['instance'])
        if self.chatbot_session_id is not None:
            self.request.set_SessionId(self.chatbot_session_id)
        result_str = self.clt.do_action_with_exception(self.request).decode('utf-8')
        self._logger.info('返回数据：'+result_str)
        result_json = json.loads(result_str)
        if self.chatbot_session_id is None:
            self.chatbot_session_id = result_json['SessionId']
        if len(result_json['Messages']) >= 1:
            return result_json['Messages'][0]['Text']['Content']
        else:
            return ''

    @classmethod
    def get_instance(cls):
        """
        返回一个实例
        :return:
        """
        return Chatbot()




