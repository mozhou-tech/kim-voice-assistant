from src.components.mic_hat.led import pixels
from importlib import util


def support_led():
    """
    检查是否支持LED
    :return:
    """
    if util.find_spec('spidev') is None:
        return False
    else:
        return True
