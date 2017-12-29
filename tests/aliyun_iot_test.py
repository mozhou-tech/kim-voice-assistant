# -*- coding: utf-8-*-
import unittest
import os
os.sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from utils.aliyun_iot.iot_wrapper import IoTWrapper
from config import profile
from utils import logger


class TestAliyunIot(unittest.TestCase):
    """

    """

    def test_init(self):
        iot_wrapper = IoTWrapper()
        iot_wrapper.main()


if __name__ == '__main__':
    logger.init(info=True)
    unittest.main()

