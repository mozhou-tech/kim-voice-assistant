# -*- coding: utf-8-*-
from utils.aliyun_fc.fc_client import FcClient
import logging
import os

logger = logging.getLogger(__name__)


def is_command_exists(command):
    """
    检查某个命令是否存在
    :param command:
    :return:
    """
    s = str(os.system(command))
    if s.endswith('command not found'):
        return False


def main():
    """
    新装设备，初始化
    :return:
    """
    # 环境检查
    if is_command_exists('play'):
        logger.info('play命令存在')

    # 函数计算
    logger.info('===============初始化函数计算==============')
    # FcClient.get_instance().init_fc_services()  # 初始化函数计算


