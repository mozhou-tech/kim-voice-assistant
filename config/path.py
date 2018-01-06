import os

APP_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

LOG_PATH = os.path.join(APP_PATH, 'data/log')

PLUGINS_PATH = os.path.join(APP_PATH, 'src/plugins')

CACHE_PATH = os.path.join(APP_PATH, 'data/cache')

CACHE_WAVE_PATH = CACHE_PATH + '/wave/'

WAVE_DING = APP_PATH + '/utils/snowboy/resources/ding.wav'
WAVE_DONG = APP_PATH + '/utils/snowboy/resources/dong.wav'

HOTWORD_MODEL_PATH = APP_PATH + '/config/hotword_models'


def get_hotword_models():
    """
    读取当前有多少个可用模型，返回
    """
    files = []
    for file in os.listdir(HOTWORD_MODEL_PATH):
        files.append(HOTWORD_MODEL_PATH + '/' + file)
    return files


HOTWORD_MODELS = get_hotword_models()
