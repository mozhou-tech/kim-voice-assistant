# -*- coding: utf-8-*-
import logging
from utils.aliyun_iotx.sign import Sign
import requests
import json
from config.path import APP_PATH
from datetime import datetime as dt
from datetime import timedelta


class IotClient:

    def __init__(self):
        self._logger = logging.getLogger()
        """
        准备客户端要求的参数
        """
        self.auth_token_cache_file_path = APP_PATH+'/utils/aliyun_iotx/resource/iot_http_auth.json'
        self.auth_token_cache_content = None
        self.endpoint = "https://iot-as-http.cn-shanghai.aliyuncs.com"
        self.path = ""
        self.topic = ""
        # 设备key和secret信息
        self.device_name = "xiaoyun001"
        self.product_key = "5ixlFmlsHNI"
        self.device_secret = "iuaUl6Z7BYnrdumO9jSIk3syzquEm7GK"

    def get_auth_token(self, refresh=False):
        """
        获得iotToken
        :param refresh 默认要求刷新token
        :return:
        """
        # 从文件缓存中获取token缓存
        if self.auth_token_cache_content is None:
            self._logger.info('读取%s缓存文件', self.auth_token_cache_file_path)
            with open(self.auth_token_cache_file_path, 'r') as f:
                self.auth_token_cache_content = json.loads(f.read())
        # 检查缓存中的token是否已经过期，过期则刷新缓存(执行异常也刷新缓存)
        if refresh:
            return self.auth_token_refresh() # 要求刷新是刷新
        else:
            try:
                if self.auth_token_cache_content['uuid'] != self.product_key+self.device_name :
                    return self.auth_token_refresh()   # 设备uuid变化时刷新
                if self.auth_token_cache_content['expired_at'] > dt.strftime(dt.now(), "%Y%m%d%H%M%S"):
                    return self.auth_token_cache_content['token']
                else:
                    return self.auth_token_refresh()  # 缓存过期时刷新
            except:
                self._logger.info("文件格式异常%s", self.auth_token_cache_file_path)
                return self.auth_token_refresh()    # 缓存格式异常时刷新

    def auth_token_build_data(self, hmacsha1='hmacsha1'):
        """
        构建Auth请求的Json
        :param hmacsha1:
        :return:
        """
        origin = {
            "deviceName" : self.device_name,
            "productKey": self.product_key
        }
        signData = Sign.get_sign(params=origin, device_secret=self.device_secret, signmethod=hmacsha1)
        return dict(origin, **{
            "version": "default",
            "clientId": signData['iot_client_id'],
            "signmethod": hmacsha1,
            "sign": signData['sign'],
            "timestamp": signData['timestamp']
        })

    def auth_token_refresh(self):
        """
        从阿里云网关重新获取iot http auth token，并缓存到文件中
        :return:
        """
        json_data = self.auth_token_build_data()
        self._logger.info('Post request %s', self.endpoint + '/auth')
        self._logger.info('Post auth data %s', json_data)
        r = requests.post(url=self.endpoint + '/auth', json=json_data, headers={
            "Content-Type": "application/json",
        })
        response_json = json.loads(r.text)
        if response_json['code'] == 0:
            self._logger.info('IoT auth success.')
            self.auth_token_cache(response_json['info']['token'])  # 将auth token写到缓存文件
            return response_json['info']['token']
        else:
            self._logger.error('IoT auth error. %s', response_json)

    def auth_token_cache(self, token):
        """
        IoT token的有效期有48小时，切访问被限制，所以需要缓存到文件中
        :return:
        """
        with open(self.auth_token_cache_file_path, 'w') as f:
            content = json.dumps({
                "uuid": self.product_key + self.device_name,
                "token": token,
                "expired_at": dt.strftime(dt.now()+timedelta(hours=40), "%Y%m%d%H%M%S")
            })
            f.write(content)

    @classmethod
    def get_instance(cls):
        return IotClient()

