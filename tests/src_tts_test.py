# -*- coding: utf-8-*-
import unittest
import os
os.sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.tts import TTSEngine
from utils import logger


class TestTTSEngine(unittest.TestCase):
    """

    """

    def setUp(self):
        self._instance = TTSEngine.get_instance()

    def test_test(self):
        print(self._instance)


if __name__ == '__main__':
    logger.init(info=True)
    unittest.main()

