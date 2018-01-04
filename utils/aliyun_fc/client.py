# -*- coding: utf-8-*-
import fc2
from config import profile
import json
import logging


class FcClient:
    """
    封装常用操作
    """
    def __init__(self):
        self._fc_client = fc2.Client(
            endpoint=profile.aliyun_fc_endpoint,
            accessKeyID=profile.ak_id,
            accessKeySecret=profile.ak_secret)
        self._logger = logging.getLogger()

    @classmethod
    def get_instance(cls):
        """
        返回FcClient实例
        :return:
        """
        return FcClient()

    def call_function(self, function_name, payload):
        """
        调用函数名称
        :param function_name:
        :param payload: 参数
        :return:
        """
        return self._fc_client.invoke_function(profile.aliyun_fc_service_name, function_name, payload=json.dumps(payload))

    def update_functions(self):
        """
        更新函数
        :return:
        """
        pass

    def create_fc_service(self):
        # 检查服务是否已存在
        exists_services = self._fc_client.list_services(prefix=profile.aliyun_fc_service_name)
        if len(exists_services.data['services']) > 0:
            self._logger.info('指定的函数计算服务已存在,%s,所在Endpoint：%s', profile.aliyun_fc_service_name, profile.aliyun_fc_endpoint)
        else:
            self._logger.info('创建函数计算服务,%s,已指定Endpoint：%s', profile.aliyun_fc_service_name, profile.aliyun_fc_endpoint)
            # 如果不存在，就创建一个函数计算服务
            result = self._fc_client.create_service(serviceName=profile.aliyun_fc_service_name,
                                                    description=profile.myname + "专用函数计算服务")
            self._logger.info('函数计算创建成功，%s', result.data)

    def memzip(self):
        """
        在内存中zip压缩代码
        :return:
        """
        pass

