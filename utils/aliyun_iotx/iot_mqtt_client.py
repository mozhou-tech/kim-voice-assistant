# -*- coding: utf-8-*-
import paho.mqtt.client as mqtt
import logging
from paho.mqtt.client import error_string
from utils.aliyun_iotx.sign import Sign
from utils.aliyun_iotx import topic
from config import device


class IotClient:

    def __init__(self):
        """
        初始化mqtt客户端
        """
        self._logger = logging.getLogger()
        self.mqtt_path = device.product_key + ".iot-as-mqtt.cn-shanghai.aliyuncs.com"  # MQTT地址
        self._topic = topic

        # 获取签名
        self.sign_dict = Sign.get_sign({
            "deviceName": device.device_name,
            "productKey": device.product_key
        }, device.device_secret)
        self.mqtt_client_id = self.sign_dict['iot_client_id'] + \
                                            "|securemode=3,signmethod=hmacsha1,timestamp=" + \
                                            self.sign_dict['timestamp'] + "|"

        self._logger.info('use mqtt device id:"%s"', self.mqtt_client_id)
        # 实例化mqtt客户端
        self._mqttc = mqtt.Client(transport="tcp", client_id=self.mqtt_client_id)

    def on_connect(self, client, userdata, flags, rc):
        self._logger.info('mqtt client is connected to server.')

    def on_publish(self, client, userdata, mid):
        self._logger.info('mqtt message published.')

    def on_subscribe(self, client, userdata, mid, rc):
        self._logger.info('mqtt message subscribe.')

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            self._logger.info("Unexpected disconnection.")
        else:
            self._logger.info('mqtt client is disconnected from server.')

    def on_message(self, client, userdata, msg):
        self._logger.info("topic " + msg.topic + " message" + str(msg.payload))

    def on_log(self, client, userdata, level, buf):
        self._logger.info('mqtt paho log %s', buf)

    def do_connect(self):
        """
        配置并建立MQTT连接
        :return:
        """
        # 设置用户名密码
        self._mqttc.username_pw_set(username=device.device_name+"&"+device.product_key, password=self.sign_dict['sign'])
        # 开启日志
        self._mqttc.enable_logger(self._logger)
        # 连接时触发
        self._mqttc.on_connect = self.on_connect
        self._mqttc.on_disconnect = self.on_disconnect
        self._mqttc.on_publish = self.on_publish
        self._mqttc.on_subscribe = self.on_subscribe
        self._mqttc.on_message = self.on_message
        self._mqttc.on_log = self.on_log
        self._logger.info('connect mqtt host: %s', self.mqtt_path)
        self._mqttc.connect(host=self.mqtt_path, port=1883, keepalive=60, bind_address='')
        self._mqttc.loop_forever()

    def do_subscribe(self, topic_name):
        self._mqttc.subscribe(self._topic.get_topic_name(topic_name))  # 订阅消息推送
        # self._mqttc.subscribe(self._topic.shadow_get)   # 订阅影子更新

    def do_publish(self, topic_name, payload, qos=0, retain=False):
        """
        向服务器发送消息
        :param topic_name: Topic名称
        :param payload:
        :param qos:
        :param retain:
        :return:
        """
        topic = self._topic.get_topic_name(topic_name)
        result = self._mqttc.publish(topic=topic, payload=payload, qos=qos, retain=retain)
        if result.is_published() is not True:
            self._logger.info('Content %s send to topic "%s" publish failed.', payload, topic)
            self._logger.info('Error string:%s', error_string(result.rc))

    def do_shadow_update(self, payload):
        """
        更新影子设备
        :return:
        """
        result = self._mqttc.publish(topic=self._topic.shadow_update, payload=payload, qos=1, retain=False)
        if result.is_published() is not True:
            self._logger.info('Content %s send to topic "%s" publish failed.', payload, self._topic.shadow_update)
            self._logger.info('Error Message:%s', error_string(result.rc))

    def do_disconnect(self):
        """
        关闭连接
        :return:
        """
        self._mqttc.disconnect()

    @classmethod
    def get_instance(cls):
        return IotClient()

