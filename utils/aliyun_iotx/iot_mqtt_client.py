# -*- coding: utf-8-*-
import paho.mqtt.client as mqtt
import logging
from utils.aliyun_iotx.sign import Sign


class IotClient:

    def __init__(self):
        """
        初始化mqtt客户端
        """
        self._logger = logging.getLogger()
        # 设备key和secret信息
        self.device_name = "xiaoyun001"
        self.product_key = "5ixlFmlsHNI"
        self.device_secret = "iuaUl6Z7BYnrdumO9jSIk3syzquEm7GK"
        self.mqtt_client_id = ''
        # MQTT地址
        self.mqtt_path = self.product_key + ".iot-as-mqtt.cn-shanghai.aliyuncs.com"
        self.topic_root = "/" + self.product_key + "/" + self.device_name

        # 获取签名
        self.sign_dict = Sign.get_sign({
            "deviceName": self.device_name,
            "productKey": self.product_key
        }, self.device_secret)
        self.mqtt_client_id = self.sign_dict['iot_client_id'] + \
                              "|securemode=3,signmethod=hmacsha1,timestamp=" + self.sign_dict['timestamp'] + "|"
        self._logger.info('use mqtt device id:"%s"', self.mqtt_client_id)
        # 实例化mqtt客户端
        self._mqttc = mqtt.Client(transport="tcp", client_id=self.mqtt_client_id)



    def on_connect(self, client, userdata, flags, rc):
        self._logger.info('mqtt client is connected to server.')
        self._mqttc.subscribe(self.topic_root+'/get')

    def on_publish(self, client, userdata, mid):
        self._logger.info('mqtt message published.')

    def on_subscribe(self, client, userdata, mid, a):
        self._logger.info('mqtt message subscribed.')

    def on_disconnect(self, client, userdata, flags, rc):
        self._logger.info('mqtt client is disconnected from server.')

    def on_message(self,client, userdata, msg):
        self._logger.info("主题:" + msg.topic + " 消息:" + str(msg.payload))

    def on_log(self, client, userdata, level, buf):
        self._logger.info('mqtt paho log %s', buf)

    def do_connect(self):
        """
        配置并建立MQTT连接
        :return:
        """
        # 设置用户名密码
        self._mqttc.username_pw_set(username=self.device_name+"&"+self.product_key, password=self.sign_dict['sign'])
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

    def do_publish(self, payload, qos=0, retain=True):
        """
        向服务器发送消息
        :param payload:
        :param qos:
        :param retain:
        :return:
        """
        topic = self.topic_root+'/update'
        result = self._mqttc.publish(topic=topic, payload=payload, qos=qos, retain=retain)
        # result = self._mqttc.subscribe(topic=topic, payload=payload, qos=qos, retain=retain)
        if result.is_published() is not True:
            self._logger.info('Content %s send to topic "%s" publish failed.', payload, topic)

    @classmethod
    def get_instance(cls):
        return IotClient()

