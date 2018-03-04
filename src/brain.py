# -*- coding: utf-8-*-

import logging
import pkgutil, os
from src.config.path import PLUGINS_PATH
import jieba
from src.components.chatbot import Chatbot
from src.config import load_yaml_settings

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler


class MyFileSystemEventHander(FileSystemEventHandler):
    def __init__(self, fn):
        super(MyFileSystemEventHander, self).__init__()
        self.restart = fn

    def on_any_event(self, event):
        if event.src_path.endswith('.py'):
            print('Python source file changed: %s' % event.src_path)
            self.restart()


class Brain:
    """
    指挥第三方插件响应，还是正常对话，还是控制
    """
    def __init__(self, mic, profile, iot_client):
        self.mic = mic
        self.profile = profile
        self._plugin_name_list = []
        self.watchdog_event_handler = MyFileSystemEventHander
        self.plugins = None
        self._logger = logging.getLogger()
        self._iot_client = iot_client
        self.handling = False
        self.chatbot = Chatbot.get_instance()
        self._custom_plugin_path = os.path.expanduser(load_yaml_settings()['custom']['plugins'])
        self.get_plugins()

    # @classmethod
    def get_plugins(self):
        """
        动态加载所有的插件，并通过优先级排序。如果插件没有定义优先级则以0看待
        """
        locations = [
            PLUGINS_PATH
        ]
        if os.path.isdir(self._custom_plugin_path):
            locations.append(self._custom_plugin_path)
            self.start_watch()       # 监听自定义插件目录的修改

        logger = logging.getLogger()
        plugins = []
        self._plugin_name_list = []
        # plugins that are not allow to be call via Wechat or Email
        logger.debug("Looking for plugins in: %s", ', '.join(["'%s'" % location for location in locations]))
        for finder, name, ispkg in pkgutil.walk_packages(locations):
            try:
                self._plugin_name_list.append(name)
                loader = finder.find_module(name)
                mod = loader.load_module(name)
            except Exception:
                logger.warning("Skipped plugin '%s' due to an error.", name, exc_info=True)
            else:
                if hasattr(mod, 'WORDS'):
                    logger.debug("Found plugin '%s' with words: %r", name, mod.WORDS)
                    plugins.append(mod)
                else:
                    logger.warning("Skipped plugin '%s' because it misses the WORDS constant.", name)
        plugins.sort(key=lambda mod: mod.PRIORITY if hasattr(mod, 'PRIORITY') else 0, reverse=True)
        logger.info('支持的插件：'+','.join(self._plugin_name_list))
        self.plugins = plugins

    def query(self, texts):
        """
        用户输入的内容传给第三方插件处理
        :param texts 用户输入内容
        :param thirdparty_call 插件内容
        """
        fenci = tuple(jieba.cut(texts))  # 对中文分词处理
        self._logger.info('word segmentation result： %s', fenci)
        for plugin in self.plugins:
            # for text in fenci:
            if plugin.is_valid(fenci):  # 判断插件是否有效
                self._logger.debug("'%s' is a valid phrase for module '%s'", texts, plugin.__name__)
                try:
                    plugin.handle(fenci, self.mic, self.profile, self._iot_client, self.chatbot)
                except Exception:
                    self._logger.error('Failed to execute plugin', exc_info=True)
                    reply = u"抱歉，我的大脑出故障了，晚点再试试吧"
                    self.mic.say(reply)
                else:
                    self._logger.debug("Handling of phrase '%s' by " +
                                       "plugin '%s' completed", texts, plugin.__name__)
                finally:
                    return
        self._logger.debug("No plugin was able to handle any of these phrases: %r", texts)

    def mod_change_detected(self):
        return LoggingEventHandler()

    def start_watch(self):
        observer = Observer()
        observer.schedule(self.watchdog_event_handler(self.get_plugins), self._custom_plugin_path, recursive=True)
        observer.start()
        self._logger.info('Watching directory %s...' % self._custom_plugin_path)



