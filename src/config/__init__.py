# -*- coding: utf-8-*-

import jieba, logging, yaml,json,os
APP_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)).replace('/src', '')

logger = logging.getLogger()

SETTING_PATH = APP_PATH + '/setting.yaml'


def load_yaml_settings():
    """
    解析配置文件
    :return:
    """
    with open(SETTING_PATH, 'r') as r:
        stream = r.read()
    return yaml.load(stream)



