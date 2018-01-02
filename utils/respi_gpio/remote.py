# -*- coding:utf-8 -*-

from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
from signal import pause


class RemoteGPIO:
    """

    """
    def __init__(self, ip_address):
        self.factory = PiGPIOFactory(host=ip_address)
        pass

    def main(self):
        pass