import unittest
import os
os.sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.plugins import Weather


class TestPluginWeather(unittest.TestCase):
    """

    """

    def test_fetch_weather_data(self):
        """
        获取天气数据
        """
        result = Weather._fetch_weather_data()


if __name__ == '__main__':
    unittest.main()

