# -*- coding: utf-8-*-
from aliyunsdkcore import client
from aliyunsdkiot.request.v20170420 import RegistDeviceRequest
from aliyunsdkiot.request.v20170420 import PubRequest
from config import profile
import logging


class IoTWrapper:
    """
    封装一下IoTKit
    """
    def __init__(self):
        self.accessKeyId = profile.ak_id
        self.accessKeySecret = profile.ak_secret
        self.productKey = '5ixlFmlsHNI'
        self._logger = logging.getLogger()

    def main(self):
        clt = client.AcsClient(self.accessKeyId, self.accessKeySecret, 'cn-shanghai')
        request = PubRequest.PubRequest()
        request.set_accept_format('json')  # 设置返回数据格式，默认为XML
        request.set_ProductKey(self.productKey)
        request.set_TopicFullName('/productKey/deviceName/get')  # 消息发送到的Topic全名
        request.set_MessageContent('aGVsbG8gd29ybGQ=')  # hello world Base64 String
        request.set_Qos(0)
        result = clt.do_action_with_exception(request)
        self._logger.info('result : %s', str(result, 'utf-8'))



