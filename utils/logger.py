# -*- coding: utf-8-*-
import logging
import os
from config.path import LOG_PATH


def init(info=False,debug=False):
    """
    args.debug   debug模式
    args.info    info模式
    :param args:
    :return:
    """
    # 创建一个logger
    logger = logging.getLogger()
    logger.propagate = False

    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler(os.path.join(LOG_PATH, "xiaoyun.log"), encoding='utf-8')

    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()

    # 定义handler的输出格式
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

    if(debug):
        ch.setLevel(logging.DEBUG)
        fh.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
        level = logging.DEBUG
    elif(info):
        ch.setLevel(logging.INFO)
        fh.setLevel(logging.INFO)
        logger.setLevel(logging.INFO)
        level = logging.INFO
    else:
        ch.setLevel(logging.ERROR)
        fh.setLevel(logging.ERROR)
        logger.setLevel(logging.ERROR)
        level = logging.ERROR

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 给logger添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)   # stream

    # 记录一条日志
    logger.info('logging module configure finished, setting level as %s.', logging.getLevelName(level))



