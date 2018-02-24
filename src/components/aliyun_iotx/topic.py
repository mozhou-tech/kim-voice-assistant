# -*- coding: utf-8-*-
from src.config import device
import logging
_logger = logging.getLogger()


def get_topic_name(topic_name='root', type='publish', is_shadow=False):
    """
    返回一个topic自定义的topic类
    :param topic_name:
    :param type
    :param is_shadow
    :return:
    """
    registered_topic = ['', 'mic_text_from_server', 'conversation_log']
    if type not in ['subscribe', 'publish']:
        raise Exception('Unsupported topic type.')
    if topic_name not in registered_topic:
        _logger.error('not registered topic')
        raise Exception('Topic："%s"未注册' % topic_name)
    else:
        if is_shadow:   # 返回影子设备
            if type == 'publish':
                return '/shadow/update/'+device.product_key+'/'+device.device_name
            elif type == 'subscribe':
                return '/shadow/get/'+device.product_key + '/' + device.device_name

        if topic_name == '' or topic_name is None or topic_name == 'root':
            return '/' + device.product_key + '/' + device.device_name
        else:
            if type == 'publish':
                return '/'+device.product_key + '/' + device.device_name + '/update_' + topic_name
            elif type == 'subscribe':
                return '/'+device.product_key + '/' + device.device_name + '/get_' + topic_name
