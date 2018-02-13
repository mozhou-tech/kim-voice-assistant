# -*- coding: utf-8-*-
import config
yaml_settings = config.load_yaml_settings()
"""
设备信息
"""
product_key = yaml_settings['aliyun']['iothub']['product_key']
device_name = yaml_settings['aliyun']['iothub']['device_name']
device_secret = yaml_settings['aliyun']['iothub']['device_secret']
