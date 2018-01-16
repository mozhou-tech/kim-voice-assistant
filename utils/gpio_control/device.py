# -*- coding: utf-8-*-
import abc


class Device:
    def __init__(self):
        self.device = None
        self.stat = None

    @abc.abstractmethod
    def sync_desire_devstat(self, payload):
        """
        同步设备状态，把desire变成现实
        :param payload
        :return:
        """

    @abc.abstractmethod
    def fetch_devstat(self):
        """
        获得设备状态
        :return:
        """

    @abc.abstractmethod
    def send_desire_stat_to_iotx(self, device, cmd):
        """
        发送预期状态给IoT设备
        :return:
        """

    @abc.abstractmethod
    def reset_device_stat(self):
        """
        重置设备
        :return:
        """

