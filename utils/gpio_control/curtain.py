# -*- coding: utf-8-*-
import RPi.GPIO as GPIO
import time
from utils.gpio_control.device import Device
from utils.aliyun_iotx.iot_mqtt_client import IotClient

IN1 = 11  # pin11
IN2 = 12
IN3 = 13
IN4 = 15

DEVICE_NAME = 'curtain'


class Curtain(Device):
    """
    窗帘
    """
    def __init__(self,iot_client):
        Device.__init__()
        assert iot_client is not None
        self._iot_client = iot_client

    def send_desire_stat_to_iotx(self, device, stat):
        """
        同步窗帘的状态到
        :return:
        """
        self._iot_client

    def get_instance(self):
        return Curtain()



def setStep(w1, w2, w3, w4):
    GPIO.output(IN1, w1)
    GPIO.output(IN2, w2)
    GPIO.output(IN3, w3)
    GPIO.output(IN4, w4)


def stop():
    setStep(0, 0, 0, 0)


def forward(delay, steps):
    for i in range(0, steps):
        setStep(1, 0, 0, 0)
        time.sleep(delay)
        setStep(0, 1, 0, 0)
        time.sleep(delay)
        setStep(0, 0, 1, 0)
        time.sleep(delay)
        setStep(0, 0, 0, 1)
        time.sleep(delay)


def backward(delay, steps):
    for i in range(0, steps):
        setStep(0, 0, 0, 1)
        time.sleep(delay)
        setStep(0, 0, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 0, 0)
        time.sleep(delay)
        setStep(1, 0, 0, 0)
        time.sleep(delay)


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)  # Numbers GPIOs by physical location
    GPIO.setup(IN1, GPIO.OUT)  # Set pin's mode is output
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)


def loop():
    while True:
        print("backward...")
        backward(0.003, 512)  # 512 steps --- 360 angle  

        print("stop...")
        stop()  # stop
        time.sleep(3)  # sleep 3s

        print("forward...")
        forward(0.005, 512)

        print("stop...")
        stop()
        time.sleep(3)


def destroy():
    GPIO.cleanup()  # Release resource


if __name__ == '__main__':  # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child function destroy() will be  executed.  
        destroy()  