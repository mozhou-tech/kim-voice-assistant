# -*- coding:utf-8 -*-

from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
import pigpio
from signal import pause


class RemoteGPIO:
    """

    """
    def __init__(self, ip_address):
        pigpio.pi()
        self.factory = PiGPIOFactory(host=ip_address, port=8888)
        pass

    def main(self):
        pass