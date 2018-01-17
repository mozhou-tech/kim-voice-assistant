from aliyunsdkcore import client
from aliyunsdkiot.request.v20170420 import RegistDeviceRequest
from aliyunsdkiot.request.v20170420 import PubRequest
from config import profile, device
import logging

class IotServer:

    def __init__(self):
        """
        初始化
        """
        self.accessKeyId = profile.ak_id
        self.accessKeySecret = profile.ak_secret
        self.clt = client.AcsClient(self.accessKeyId, self.accessKeySecret, 'cn-shanghai')
        self.request = PubRequest.PubRequest()
        self.request.set_accept_format('json')  # 设置返回数据格式，默认为XML
        self.request.set_ProductKey(device.product_key)
        self._logger = logging.getLogger()

    def send_device_desired(self, topic, payload):
        """
        发送设备期望状态
        :return:
        """
        self.request.set_TopicFullName(topic)  #消息发送到的Topic全名
        self.request.set_MessageContent(payload)  #hello world Base64 String
        self.request.set_Qos(0)
        result = self.clt.do_action_with_exception(self.request)
        self._logger.info('iot-server result : ' + result)

    @classmethod
    def get_instance(cls):
        return IotServer()
