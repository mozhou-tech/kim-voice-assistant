from gpiozero import RGBLED
from time import sleep

led = RGBLED(red=9, green=10, blue=11)

while True:
    led.color = (0, 0, 0)
