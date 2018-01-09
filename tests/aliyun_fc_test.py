# -*- coding: utf-8-*-
import unittest
import os
os.sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from utils import logger
import logging
from utils.aliyun_fc.fc_client import FcClient
import json
import wave
import time
from config.path import CACHE_WAVE_PATH
from src.tts import TTSEngine


class TestAliyunFc(unittest.TestCase):
    """
    函数计算单元测试
    """
    def setUp(self):
        self._logger = logging.getLogger()
        self.fc_client = FcClient.get_instance()

    def atest_init_service(self):
        """
        检查函数计算服务是否已存在
        :return:
        """
        self.fc_client.create_fc_service()

    def atest_update_and_call_function_for_api_market(self):
        """
        调用函数计算服务，从API中读取数据
        :return:
        """
        self.fc_client.update_functions('aliyun_apimarket')
        # 获取天气预报的Payload
        payload = {
            'host': 'http://freecityid.market.alicloudapi.com',
            'path': '/whapi/json/alicityweather/briefforecast3days',
            'method': 'POST',
            'appcode': 'cd08e261838a42328340f49cd28c02b4',
            'payload': {
                'cityId': '1045'
            },
            'bodys': {},
            'querys': ''
        }
        # 获取新闻头条的Payload
        # payload = {
        #     'host': 'http://topnews.market.alicloudapi.com',
        #     'path': '/toutiao/index',
        #     'method': 'GET',
        #     'appcode': 'cd08e261838a42328340f49cd28c02b4',
        #     'payload': {
        #         'type': 'top'
        #     },
        #     'bodys': {},
        #     'querys': ''
        # }
        result = self.fc_client.call_function('aliyun_apimarket', payload=payload)
        result = json.loads(result.data)
        self._logger.info(result)

    def test_update_and_call_function_for_asr(self):
        """
        语音识别
        :return:
        """
        self.fc_client.update_functions('aliyun_nls_asr')
        fp = CACHE_WAVE_PATH + 'record_output.wav'
        try:
            wav_file = wave.open(fp, 'rb')
        except IOError:
            self._logger.critical('wav file not found: %s', fp, exc_info=True)
            return
        n_frames = wav_file.getnframes()
        audio = wav_file.readframes(n_frames)
        time_start = time.time()
        result = self.fc_client.call_function('aliyun_nls_asr', payload=audio)
        time_end = time.time()
        # 返回的bytes流保存到wav音频文件
        # assert result.headers['Content-Type'] == 'application/octet-stream'  # 验证返回数据正确性
        self._logger.info('文字识别完成，接口耗时%ss', round(time_end - time_start, 2))
        print(result.data.decode('utf8'))

    def atest_update_and_call_function_for_tts(self):
        """
        语音合成
        :return:
        """
        self.fc_client.update_functions('aliyun_nls_tts')
        payload = {
            'text': '你说啥'
        }
        time_start = time.time()
        result = self.fc_client.call_function('aliyun_nls_tts', payload)
        time_end = time.time()
        # 返回的bytes流保存到wav音频文件
        assert result.headers['Content-Type'] == 'application/octet-stream'  # 验证返回数据正确性
        self._logger.info('音频已生成，接口耗时%ss', round(time_end-time_start, 2))
        tts_engine = TTSEngine.get_instance()
        b, wave_pathname = tts_engine.get_speech_cache(payload['text'])
        with open(wave_pathname, 'wb') as f:
            f.write(result.data)
        os.system('play '+wave_pathname)


if __name__ == '__main__':
    logger.init(info=True)
    unittest.main()


