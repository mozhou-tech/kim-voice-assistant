# -*- coding: utf-8-*-
import unittest
import os,jieba
os.sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.plugins import Weather,WakeUpBell,Joke
from src.components import logger
from src.components.homeassistant import conn

class TestHaConn(unittest.TestCase):
    """

    """
    def setUp(self):
        pass

    def test_connection(self):
        conn.connection()

if __name__ == '__main__':
    logger.init(info=True)
    unittest.main()

