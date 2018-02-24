# -*- coding: utf-8-*-
from src.components.aliyun_fc.fc_client import FcClient
import time,logging,json


class ASREngine:
    """
    语音识别模块
    """
    def __init__(self, fc_client):
        """
        init
        :param over_iothub: 是否通过iot套件
        """
        self._fc_client = fc_client
        self._logger = logging.getLogger()

    @classmethod
    def get_instance(cls):
        """
        返回一个ASR实例
        :return:
        """
        return ASREngine(FcClient.get_instance())

    def wave_to_text(self, wave_path):
        """
        输入音频路径，返回转换结果
        :param wave_path:
        :return:
        """
        with open(wave_path, 'rb') as f:
            wave_data = f.read()
        start_time = time.time()
        result = self._fc_client.call_function('aliyun_nls_asr', payload=wave_data)
        end_time = time.time()
        self._logger.info('语音转文字完成，耗时 %ss.', round(end_time-start_time, 3))
        data = json.loads(result.data.decode('utf8'))
        if data['status'] == "SUCCEED":
            self._logger.info('语音识别结果: %s', data['result'])
            return data['result']
        else:
            return False


