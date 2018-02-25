# -*- coding: utf-8-*-

import logging
import pkgutil
from src.config.path import PLUGINS_PATH
import jieba
from src.components.chatbot import Chatbot


class Brain:
    """
    指挥第三方插件响应，还是正常对话，还是控制
    """
    def __init__(self, mic, profile, iot_client):
        self.mic = mic
        self.profile = profile
        self.plugins = self.get_plugins()
        self._logger = logging.getLogger()
        self._iot_client = iot_client
        self.handling = False
        self.chatbot = Chatbot.get_instance()

    @classmethod
    def get_plugins(cls):
        """
        动态加载所有的插件，并通过优先级排序。如果插件没有定义优先级则以0看待
        """
        locations = [
            PLUGINS_PATH
        ]
        logger = logging.getLogger()
        plugins = []
        # plugins that are not allow to be call via Wechat or Email
        logger.debug("Looking for plugins in: %s", ', '.join(["'%s'" % location for location in locations]))
        for finder, name, ispkg in pkgutil.walk_packages(locations):
            try:
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
        return plugins

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



