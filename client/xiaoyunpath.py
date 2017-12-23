# -*- coding: utf-8-*-
import os

APP_PATH = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir))

DATA_PATH = os.path.join(APP_PATH, "data/static")
LIB_PATH = os.path.join(APP_PATH, "client")
LOGIN_PATH = os.path.join(APP_PATH, "login")
TEMP_PATH = os.path.join(APP_PATH, "temp")
LOG_PATH = os.path.join(APP_PATH, "data/log")
PLUGIN_PATH = os.path.join(LIB_PATH, "plugins")

CONFIG_PATH = os.path.join(APP_PATH, "data/config")
CONTRIB_PATH = os.path.join(APP_PATH,  "contrib")
CUSTOM_PATH = os.path.join(APP_PATH, "custom")


def config(*fname):
    return os.path.join(CONFIG_PATH, *fname)


def data(*fname):
    return os.path.join(DATA_PATH, *fname)
