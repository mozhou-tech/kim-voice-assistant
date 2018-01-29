# -*- coding: utf-8-*-
from utils.aliyun_fc.fc_client import FcClient
import logging
import subprocess
import os

logger = logging.getLogger()


def is_command_exists(command):
    """
    检查某个命令是否存在
    :param command:
    :return:
    """

    s = str(subprocess.check_output([command, '--help']))
    if s.endswith('command not found'):
        return False
    return True


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
    FcClient.get_instance().init_fc_services()  # 初始化函数计算


def install_aliyun_service():
    pass


