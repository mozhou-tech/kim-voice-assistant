# -*- coding: utf-8-*-
import paho.mqtt.client as mqtt
import logging
from utils.aliyun_iotx.sign import Sign


class IotClient:

    def __init__(self):
        self._logger = logging.getLogger()
        """
        准备客户端要求的参数
        """
        self.auth_url = "https://iot-auth.cn-shanghai.aliyuncs.com/auth/devicename"
        # 设备key和secret信息
        self.device_name = "xiaoyun001"
        self.product_key = "5ixlFmlsHNI"
        self.device_secret = "iuaUl6Z7BYnrdumO9jSIk3syzquEm7GK"
        # MQTT地址
        self.mqtt_path = self.product_key + ".iot-as-mqtt.cn-shanghai.aliyuncs.com"
        # 用于测试的Topic
        self.sub_topic = "/" + self.product_key + "/" + self.device_name + "/get"
        self.pub_topic = "/" + self.product_key + "/" + self.device_name + "/update"
        # 设备影子topic
        self.shadow_ack_topic = "/shadow/get/" + self.product_key + "/" + self.device_name
        self.shadow_update_topic = "/shadow/update/" + self.product_key + "/" + self.device_name
        self.shadow_version = 0
        self._mqttc = mqtt.Client(transport="tcp")


    def connect_mqtt(self):
        """
        连接MQTT
        :return:
        """
        self._mqttc.enable_logger(self._logger)
        self._mqttc.user_data_set({

        })
        sign_str = Sign.get_sign(self.device_name, self.device_secret, self.product_key)
        self._mqttc.username_pw_set(self.device_name+"&"+self.product_key, sign_str)
        self._mqttc.connect(self.mqtt_path, 1883, 60)
        self._mqttc.subscribe("$SYS/#", 0)
        self._mqttc.loop_forever()

    @classmethod
    def get_instance(cls):
        return IotClient()

