import os
from src.config import load_yaml_settings

APP_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)).replace('/src', '')

APP_RESOURCES_DATA_PATH = APP_PATH + '/data/resources/'

LOG_PATH = os.path.join(APP_PATH, 'data/log')

PLUGINS_PATH = os.path.join(APP_PATH, 'src/plugins')

CACHE_PATH = os.path.join(APP_PATH, 'data/cache')

CACHE_WAVE_PATH = CACHE_PATH + '/wave/'

CACHE_WAVE_RECORDED = CACHE_WAVE_PATH + '/record_output.wav'
"""
常用的wave声音
"""
WAVE_DING = APP_PATH + '/src/components/snowboy/resources/ding.wav'
WAVE_DONG = APP_PATH + '/src/components/snowboy/resources/dong.wav'

HOTWORD_MODEL_PATH = APP_PATH + '/src/config/hotword_models'


def get_hotword_models():
    """
    读取当前有多少个可用模型，返回
    """
    custom_dir = os.path.expanduser(load_yaml_settings()['custom']['hotwords'])
    file_list = []
    if os.path.exists(custom_dir):
        file_list = file_list + os.listdir(custom_dir)
    file_list = file_list + os.listdir(HOTWORD_MODEL_PATH)
    files = []
    for file in file_list:
        if file.endswith('umdl') or file.endswith('pmdl'):   # 限制模型类型
            if os.path.isfile(HOTWORD_MODEL_PATH + '/' + file):
                files.append(HOTWORD_MODEL_PATH + '/' + file)
            if os.path.isfile(custom_dir + '/' + file):
                files.append(custom_dir + '/' + file)
    if len(files) == 0:
        raise Exception('你至少应该有一个热词模型，请参照README.md')
    return files


HOTWORD_MODELS = get_hotword_models()
