# -*- coding: utf-8-*-
from utils.aliyun_fc.fc_client import FcClient
import logging

logger = logging.getLogger()


def main():
    """
    新装设备，初始化
    :return:
    """
    logger.info('===============初始化函数计算==============')
    FcClient.get_instance().init_fc_services()  # 初始化函数计算


