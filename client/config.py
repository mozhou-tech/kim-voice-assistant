import os

APP_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         os.pardir))



"""
System
"""
LIB_PATH = os.path.join(APP_PATH, "client")
PLUGIN_PATH = os.path.join(LIB_PATH, "plugins")

"""
Config
"""
CONFIG_PATH = os.path.join(APP_PATH, "data/config")
"""
Data Cache Log
"""
CACHE_WX_PATH = os.path.join(APP_PATH, "data/cache/wxbot")
CONTRIB_PATH = os.path.join(APP_PATH,  "contrib")
CUSTOM_PATH = os.path.join(APP_PATH, "custom")
LOG_PATH = os.path.join(APP_PATH, "data/log")
DATA_PATH = os.path.join(APP_PATH, "data/static")
LOGIN_PATH = os.path.join(APP_PATH, "data/login")



def config(*fname):
    return os.path.join(CONFIG_PATH, *fname)


def data(*fname):
    return os.path.join(DATA_PATH, *fname)
