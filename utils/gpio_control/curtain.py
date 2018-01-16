# -*- coding: utf-8-*-
# import RPi.GPIO as GPIO
import time
from utils.gpio_control.device import Device
from utils.aliyun_iotx.iot_mqtt_client import IotClient
import logging,json
from config.path import APP_RESOURCES_DATA_PATH

IN1 = 11  # pin11
IN2 = 12
IN3 = 13
IN4 = 15

DEVICE_NAME = 'curtain'  # 状态值  1-100
SUPPORTED_CMD = ['open', 'close', 'open-to-half', 'close-to-half', 'open-little-more', 'close-little-more']


class Curtain(Device):
    """
    窗帘
    """
    def __init__(self, iot_client):
        Device.__init__(self)
        assert iot_client is not None
        assert isinstance(SUPPORTED_CMD, list)
        assert isinstance(DEVICE_NAME, str)

        self._iot_client = iot_client
        self._logger = logging.getLogger()
        self.open_percentage = self.get_open_percentage()

    def send_desire_stat_to_iotx(self, device, cmd):
        """
        同步窗帘的状态到IoTub
        :return:
        """
        # cmd转为窗帘打开的比例
        if cmd == 'open':
            self.open_percentage = 100
        elif cmd == 'close':
            self.open_percentage = 0
        elif cmd == 'open-to-half' or cmd == 'close-to-half':
            self.open_percentage = 50
        elif cmd == 'open-little-more':
            self.open_percentage = self.get_open_percentage() + 10
        elif cmd == 'close-little-more':
            self.open_percentage = self.get_open_percentage() - 10

        # 更新设备期望状态文件
        with open(APP_RESOURCES_DATA_PATH + 'iotx_devstat/desire_for_iot.json', mode='r+') as f:
            desire_devstat_json = json.loads(f.read())
            desire_devstat_json['state']['desired'][DEVICE_NAME] = self.open_percentage
            f.seek(0)
            f.write(json.dumps(desire_devstat_json) + '                        ')

        self._iot_client.do_desire_devstat(version_increase=True)

    @classmethod
    def get_instance(cls, iot_client):
        return Curtain(iot_client)

    def get_open_percentage(self):
        """
        获取当前窗帘打开的比例
        :return:
        """
        with open(APP_RESOURCES_DATA_PATH + 'iotx_devstat/report_for_iot.json', mode='r') as f:
            iot_desire_json = json.loads(f.read())
        return int(iot_desire_json['state']['reported'][DEVICE_NAME])


#
# def setStep(w1, w2, w3, w4):
#     GPIO.output(IN1, w1)
#     GPIO.output(IN2, w2)
#     GPIO.output(IN3, w3)
#     GPIO.output(IN4, w4)
#
#
# def stop():
#     setStep(0, 0, 0, 0)
#
#
# def forward(delay, steps):
#     for i in range(0, steps):
#         setStep(1, 0, 0, 0)
#         time.sleep(delay)
#         setStep(0, 1, 0, 0)
#         time.sleep(delay)
#         setStep(0, 0, 1, 0)
#         time.sleep(delay)
#         setStep(0, 0, 0, 1)
#         time.sleep(delay)
#
#
# def backward(delay, steps):
#     for i in range(0, steps):
#         setStep(0, 0, 0, 1)
#         time.sleep(delay)
#         setStep(0, 0, 1, 0)
#         time.sleep(delay)
#         setStep(0, 1, 0, 0)
#         time.sleep(delay)
#         setStep(1, 0, 0, 0)
#         time.sleep(delay)
#
#
# def setup():
#     GPIO.setwarnings(False)
#     GPIO.setmode(GPIO.BOARD)  # Numbers GPIOs by physical location
#     GPIO.setup(IN1, GPIO.OUT)  # Set pin's mode is output
#     GPIO.setup(IN2, GPIO.OUT)
#     GPIO.setup(IN3, GPIO.OUT)
#     GPIO.setup(IN4, GPIO.OUT)
#
#
# def loop():
#     while True:
#         print("backward...")
#         backward(0.003, 512)  # 512 steps --- 360 angle
#
#         print("stop...")
#         stop()  # stop
#         time.sleep(3)  # sleep 3s
#
#         print("forward...")
#         forward(0.005, 512)
#
#         print("stop...")
#         stop()
#         time.sleep(3)
#
#
# def destroy():
#     GPIO.cleanup()  # Release resource
#
#
# if __name__ == '__main__':  # Program start from here
#     setup()
#     try:
#         loop()
#     except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child function destroy() will be  executed.
#         destroy()