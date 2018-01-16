# -*- coding: utf-8-*-
import abc


class Device:
    @abc.abstractmethod
    def realize(self, payload):
        """
        实现设备状态，
        :param payload
        :return:
        """
    @abc.abstractmethod
    def fetch_origin_from_device(self):
        """
        获得设备状态
        :return:
        """

    @abc.abstractmethod
    def send_desire_to_iot(self):
        """
        发送
        :return:
        """

    @abc.abstractmethod
    def reset_device(self):
        """
        重置设备
        :return:
        """
