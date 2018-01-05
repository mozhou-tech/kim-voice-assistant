import os

APP_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

LOG_PATH = os.path.join(APP_PATH, 'data/log')

PLUGINS_PATH = os.path.join(APP_PATH, 'src/plugins')

CACHE_PATH = os.path.join(APP_PATH, 'data/cache')

CACHE_WAVE_PATH = CACHE_PATH + '/wave/'
