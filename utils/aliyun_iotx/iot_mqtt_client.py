# -*- coding: utf-8-*-
import paho.mqtt.client as mqtt
import logging
from paho.mqtt.client import error_string
from utils.aliyun_iotx.sign import Sign
from utils.aliyun_iotx import topic
from config import device
from config.path import APP_RESOURCES_DATA_PATH
import json


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

    def do_subscribe(self, topic_name='', is_shadow=False):
        """
        订阅Topic
        :param topic_name:
        :param is_shadow:
        :return:
        """
        self._mqttc.subscribe(self._topic.get_topic_name(topic_name, type='subscribe', is_shadow=is_shadow))  # 订阅消息推送

    def do_publish(self, topic_name='', payload='', qos=0, retain=False, is_shadow=False):
        """
        向服务器发送消息
        :param topic_name: Topic名称
        :param payload:
        :param qos:
        :param retain:
        :param is_shadow  是否是影子设备
        :return:
        """
        topic = self._topic.get_topic_name(topic_name, type='publish', is_shadow=is_shadow)

        result = self._mqttc.publish(topic=topic, payload=payload, qos=qos, retain=retain)
        if result.is_published() is not True:
            self._logger.info('Content %s send to topic "%s" publish failed.', payload, topic)
            self._logger.info('Error string:%s', error_string(result.rc))

    def _get_last_shadow_version(self):
        """
        获取最新的设备影子的版本号
        :return:
        """
        with open(APP_RESOURCES_DATA_PATH + 'iotx_devstat/report_for_iot.json', mode='r') as f:
            report_devstat = json.loads(f.read())
        with open(APP_RESOURCES_DATA_PATH + 'iotx_devstat/desire_for_iot.json', mode='r') as f:
            desire_devstat = json.loads(f.read())
        if desire_devstat['version'] > report_devstat['version']:
            return desire_devstat['version']
        return report_devstat['version']

    def do_report_devstat(self, version_increase=False):
        """
        上报设备状态
        :return:
        """
        self._logger.info('上报设备状态')
        with open(APP_RESOURCES_DATA_PATH + 'iotx_devstat/report_for_iot.json', mode='r') as f:
            devstat_str = f.read()
        if version_increase:        # 修改devstat文件
            devstat_json = json.loads(devstat_str)
            devstat_json['version'] = self._get_last_shadow_version() + 1
            devstat_str = json.dumps(devstat_json)
            with open(APP_RESOURCES_DATA_PATH + 'iotx_devstat/report_for_iot.json', mode='w') as f:
                f.write(devstat_str)
        # self.do_subscribe(is_shadow=True)  # 订阅
        self.do_publish(payload=devstat_str, is_shadow=True)

    def do_desire_devstat(self, version_increase=False):
        """
        发送期望的设备状态
        :return:
        """
        self._logger.info('发送期望的设备状态')
        with open(APP_RESOURCES_DATA_PATH + 'iotx_devstat/desire_for_iot.json', mode='r') as f:
            devstat_str = f.read()
        if version_increase:  # 修改devstat文件
            devstat_json = json.loads(devstat_str)
            devstat_json['version'] = self._get_last_shadow_version() + 1
            devstat_str = json.dumps(devstat_json)
            with open(APP_RESOURCES_DATA_PATH + 'iotx_devstat/desire_for_iot.json', mode='w') as f:
                f.write(devstat_str)
            # self.do_subscribe(is_shadow=True)  # 订阅
        self.do_publish(payload=devstat_str, is_shadow=True)

    def do_get_devstat(self):
        """
        要求返回设备状态
        :return:
        """
        up_data = '{"method": "get"}'
        self.do_publish(payload=up_data, is_shadow=True)

    def do_disconnect(self):
        """
        关闭连接
        :return:
        """
        self._mqttc.disconnect()

    @classmethod
    def get_instance(cls):
        return IotClient()

