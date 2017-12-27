import logging


class Brain:
    """
    指挥第三方插件响应，还是正常对话，还是控制
    """
    def __init__(self, mic):
        self.mic = mic
        # (self.plugins, self.exclude_plugins) = self.get_plugins()
        self._logger = logging.getLogger(__name__)
        self.handling = False

    @classmethod
    def get_plugins(cls):
        """
        动态加载所有的插件，并通过优先级排序。如果插件没有定义优先级则以0看待
        """
        return


    def isEnabled(self, plugin):
        """
        插件是否可用
        :param plugin:
        :return:
        """
        pass


    def query(self, texts, thirdparty_call=False):
        """
        Passes user input to the appropriate plugin, testing it against
        each candidate plugin's isValid function.

        Arguments:
        text -- user input, typically speech, to be parsed by a plugin
        send_wechat -- also send the respondsed result to wechat
        """
        pass


