from aliyunsdkcore import client
from aliyunsdkiot.request.v20170420 import RegistDeviceRequest
from aliyunsdkiot.request.v20170420 import PubRequest
from config import profile, device
import logging,json,base64


class IotServer:

    def __init__(self):
        """
        初始化
        """
        self.accessKeyId = profile.ak_id
        self.accessKeySecret = profile.ak_secret
        self._logger = logging.getLogger()

    def send_device_desired(self, topic, payload):
        """
        发送设备期望状态
        :return:
        """
        print(topic)
        print(device.product_key)
        self.clt = client.AcsClient(self.accessKeyId, self.accessKeySecret, 'cn-shanghai')
        self.request = PubRequest.PubRequest()
        self.request.set_accept_format('json')  # 设置返回数据格式，默认为XML
        self.request.set_ProductKey(device.product_key)
        self.request.set_TopicFullName(topic)  #消息发送到的Topic全名
        self.request.set_MessageContent(base64.b64encode(payload.encode('utf8')))  #hello world Base64 String
        self.request.set_Qos(1)
        result_json = json.loads(self.clt.do_action_with_exception(self.request).decode('utf8'))
        if result_json['Success']:
            self._logger.info('device desired send successed %s.', result_json['RequestId'])
        else:
            self._logger.error(result_json['ErrorMessage']+'RequestId:'+result_json['RequestId'])
        # self._logger.info('iot-server result : ' + result)

    @classmethod
    def get_instance(cls):
        return IotServer()
