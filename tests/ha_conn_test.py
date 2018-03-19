# -*- coding: utf-8-*-
import unittest
import os,jieba, time
os.sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.plugins import Weather,WakeUpBell,Joke
from src.config import load_yaml_settings
from src.components import logger
from src.components.homeassistant import Hass


class TestHaConn(unittest.TestCase):
    """

    """
    def setUp(self):
        pass

    def test_connection(self):
        entity_id = load_yaml_settings()['hass']['entities']['xiaomi']['gateway_light']
        hass = Hass.get_instance()
        hass.conn()
        hass.xiaomi_gateway_light(entity_id=entity_id, state='turn_on', rgb_color=[255, 100, 100], brightness=10)
        time.sleep(0.5)
        hass.xiaomi_gateway_light(entity_id=entity_id, state='turn_off')
        hass.xiaomi_print_entities()


if __name__ == '__main__':
    logger.init(info=True)
    unittest.main()

