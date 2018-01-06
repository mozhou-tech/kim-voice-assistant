# -*- coding: utf-8-*-
import fc2
from config import profile
import json
import logging
from config import path
import time
import base64

functions_map = {
    'api_market': {
        'description': '云市场API',
    },
    'speech_interaction': {
        'description': '语音交互，包含TTS/ASR/对话',
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
        if payload.get('wave_bytes'):
            # print(payload.get('wave_bytes'))
            payload['wave_bytes'] = base64.b64encode(payload['wave_bytes']).decode('utf-8')
        return self._fc_client.invoke_function(profile.aliyun_fc_service_name,
                                               function_name,
                                               payload=json.dumps(payload))

    def update_functions(self, function_name):
        """
        更新函数
        :return:
        """
        exists_functions = self._fc_client.list_functions(serviceName=profile.aliyun_fc_service_name,
                                                          prefix=function_name)
        code_dir = FUNCTION_PATH+'/'+function_name
        self._logger.info('use function code dir: %s', code_dir)

        # 更新包之前，先准备根目录下的appsecret.json文件
        with open(code_dir+'/appsecret.json', 'w') as f:
            f.write(json.dumps({
                'ak_id': profile.ak_id,
                'ak_secret': profile.ak_secret
            }))

        # 判断指定函数是否已存在，存在则更新，没有就创建
        if len(exists_functions.data['functions']) == 0:
            self._logger.info('函数计算服务%s中不存在指定函数%s即将创建', profile.aliyun_fc_service_name, function_name)
            self._fc_client.create_function(serviceName=profile.aliyun_fc_service_name,
                                            description=functions_map[function_name]['description'],
                                            functionName=function_name,
                                            codeDir=code_dir,
                                            runtime='python3',
                                            handler='main.my_handler')
        else:
            self._fc_client.update_function(serviceName=profile.aliyun_fc_service_name,
                                            functionName=function_name,
                                            codeDir=code_dir,
                                            description=functions_map[function_name]['description'])
        self._logger.info('function "%s" in "%s" updated.', function_name,profile.aliyun_fc_service_name)

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



