# -*- coding: utf-8-*-
import paho.mqtt.client as mqtt
import logging
from utils.aliyun_iotx.sign import Sign
from paho.mqtt import subscribe


class IotClient():

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
        self.mqtt_client_id = ''
        self._mqttc = ''
        # MQTT地址
        self.mqtt_path = self.product_key + ".iot-as-mqtt.cn-shanghai.aliyuncs.com"
        self.topic_root = "/" + self.product_key + "/" + self.device_name

        # 设备影子topic
        self.shadow_ack_topic = "/shadow/get/" + self.product_key + "/" + self.device_name
        self.shadow_update_topic = "/shadow/update/" + self.product_key + "/" + self.device_name
        self.shadow_version = 0

    def on_connect(self, client, userdata, flags, rc):
        self._logger.info('mqtt client is connected to server.')

    def on_publish(self, client, userdata, mid):
        self._logger.info('message published.')

    def on_subscribe(self, client, userdata, mid):
        self._logger.info('message subscribed.')

    def on_disconnect(self, client, userdata, flags, rc):
        self._logger.info('mqtt client is disconnected from server.')

    def connect_mqtt(self):
        """
        配置并建立MQTT连接
        :return:
        """
        # 获取签名
        sign_str = Sign.get_sign({
            "deviceName": self.device_name,
            "productKey": self.product_key
        }, self.device_secret)
        self.mqtt_client_id = sign_str['iot_client_id'] + \
                              "|securemode=3,signmethod=hmacsha1,timestamp="+sign_str['timestamp']+"|"
        self._logger.info('use mqtt device id:"%s"', self.mqtt_client_id)
        # 实例化mqtt客户端
        self._mqttc = mqtt.Client(transport="tcp", client_id=self.mqtt_client_id)
        # 设置用户名密码
        self._mqttc.username_pw_set(username=self.device_name+"&"+self.product_key, password=sign_str['sign'])
        # 开启日志
        self._mqttc.enable_logger(self._logger)
        # 连接时触发
        self._mqttc.on_connect = self.on_connect
        self._mqttc.on_disconnect = self.on_disconnect
        self._mqttc.on_publish = self.on_publish
        self._mqttc.on_subscribe = self.on_subscribe
        self._logger.info('connect mqtt host: %s', self.mqtt_path)
        self._mqttc.connect(host=self.mqtt_path, port=1883, keepalive=60)
        self._mqttc.loop_forever()

    @classmethod
    def get_instance(cls):
        return IotClient()

