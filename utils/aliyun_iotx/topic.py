# -*- coding: utf-8-*-
from config import device
import logging
_logger = logging.getLogger(__name__)

# 更新设备影子状态
shadow_update = '/shadow/update/'+device.product_key+'/'+device.device_name
# 获取设备影子状态
shadow_get = '/shadow/get/'+device.product_key + '/' + device.device_name


def get_topic_name(topic_name='root', type = 'publish'):
    """
    返回一个topic自定义的topic类
    :param topic_name:
    :return:
    """
    registered_topic = [
        'fc_asr', 'fc_tts', 'fc_api_market', 'fc_device_log'
    ]
    if type not in ['subscribe','publish']:
        raise Exception('Unsupported topic type.')
    if topic_name not in registered_topic:
        _logger.error('not registered topic')
        raise Exception('Topic："%s"未注册' % topic_name)
    else:
        if topic_name == '' or topic_name is None or topic_name == 'root':
            return '/' + device.product_key + '/' + device.device_name
        else:
            if type == 'publish':
                return '/'+device.product_key + '/' + device.device_name + '/' + topic_name + '_update'
            elif type == 'subscribe':
                return '/'+device.product_key + '/' + device.device_name + '/' + topic_name + '_get'
