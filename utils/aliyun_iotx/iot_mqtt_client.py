# -*- coding: utf-8-*-
import paho.mqtt.client as mqtt
import logging
from paho.mqtt.client import error_string
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
        # 影子设备Topic
        self.topic_shadow_update = '/shadow/update/'+self.product_key+'/'+self.device_name
        self.topic_shadow_get = '/shadow/get/'+self.product_key+'/'+self.device_name

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


    def on_publish(self, client, userdata, mid):
        self._logger.info('mqtt message published.')

    def on_subscribe(self, client, userdata, mid, a):
        self._logger.info('mqtt message subscribed.')

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            self._logger.info("Unexpected disconnection.")
        else:
            self._logger.info('mqtt client is disconnected from server.')

    def on_message(self,client, userdata, msg):
        self._logger.info("topic " + msg.topic + " message" + str(msg.payload))

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

    def do_subscribe(self):
        self._mqttc.subscribe(self.topic_root+'/get')  # 订阅消息推送
        self._mqttc.subscribe(self.topic_shadow_get)   # 订阅影子更新

    def do_publish(self, payload, qos=0, retain=False):
        """
        向服务器发送消息
        :param payload:
        :param qos:
        :param retain:
        :return:
        """
        topic = self.topic_root+'/update'
        result = self._mqttc.publish(topic=topic, payload=payload, qos=qos, retain=retain)
        if result.is_published() is not True:
            self._logger.info('Content %s send to topic "%s" publish failed.', payload, topic)
            self._logger.info('Error string:%s', error_string(result.rc))

    def do_shadow_update(self, payload):
        """
        更新影子设备
        :return:
        """
        result = self._mqttc.publish(topic=self.topic_shadow_update, payload=payload, qos=1, retain=False)
        if result.is_published() is not True:
            self._logger.info('Content %s send to topic "%s" publish failed.', payload, self.topic_shadow_update)
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

