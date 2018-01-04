# -*- coding: utf-8-*-
import fc2
from config import profile
import json
import logging
import zipfile
from config import path
from utils.aliyun_fc.memory_zip import MemoryZip
import time

functions_map = {
    'api_market': {
        'description': '云市场API',
        'files': ('main.py')
    },
    'speech_interaction': {
        'description': '语音交互，包含TTS/ASR/对话',
        'files': ('asr.py', 'main.py', 'sign.py', 'tts.py')
    }
}

FUNCTION_PATH = path.APP_PATH + '/utils/aliyun_fc/functions'


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

    def update_functions(self, function_name):
        """
        更新函数
        :return:
        """
        exists_functions = self._fc_client.list_functions(serviceName=profile.aliyun_fc_service_name,
                                                          prefix=function_name)
        zipfile_path = self.memzip(function_name)
        time.sleep(1)
        if len(exists_functions.data['functions']) == 0:
            self._logger.info('函数计算服务%s中不存在指定函数%s即将创建', profile.aliyun_fc_service_name, function_name)
            self._fc_client.create_function(serviceName=profile.aliyun_fc_service_name,
                                            description='',
                                            functionName=function_name,
                                            codeZipFile=zipfile_path,
                                            runtime='python3',
                                            handler='handler')
        else:
            self._fc_client.update_function(serviceName=profile.aliyun_fc_service_name,
                                            functionName=function_name,
                                            codeZipFile=zipfile_path,
                                            description=functions_map[function_name])

    def create_fc_service(self):
        """
        检查函数服务是否已存在，不存在则按照配置创建一个
        :return:
        """
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

    def memzip(self, function_name):
        """
        在内存中zip压缩代码,并保存到缓存目录中
        :param: function_name
        :return:
        """
        mz = MemoryZip()
        cachepath = path.CACHE_PATH + '/zip/' + function_name + '.zip'
        self._logger.info('zip file cache path %s.',cachepath)
        for file in functions_map[function_name]['files']:
            function_pathname = FUNCTION_PATH + '/' + function_name + '/' + file
            self._logger.info(function_pathname)
            with open(function_pathname, 'r') as f:
                mz.append(file, f.read())
        mz.save(cachepath)
        return cachepath



