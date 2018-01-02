# -*- coding: utf-8-*-
import unittest
import os
os.sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from utils.respi_gpio.remote import RemoteGPIO
from utils import logger


class TestPluginWeather(unittest.TestCase):
    """

    """

    def setUp(self):
        self._instance = RemoteGPIO(ip_address='192.168.17.152')

    def factory_test(self):
        print(self._instance)



if __name__ == '__main__':
    logger.init(info=True)
    unittest.main()

