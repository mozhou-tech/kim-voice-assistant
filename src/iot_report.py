# -*- coding: utf-8-*-
import json,socket
from config.path import APP_RESOURCES_DATA_PATH
from config.profile import myname,timezone,city,\
    remote_control_service_enable,remote_control_password,remote_control_api_token
"""
组织用于报告给Iothub的数据
"""


def save_shadow_kvs_for_settings():
    """
    设备信息报告到report_for_iot准备上传给影子设备
    :param iot_client:
    :param kvs:
    :return:
    """
    """
    获取IP地址
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    kvs = {
        'cfg_myname': myname,
        'cfg_timezone': timezone,
        'cfg_city': city,
        'cfg_remote_control_service_enable': remote_control_service_enable,
        'cfg_remote_control_password': remote_control_password,
        'cfg_remote_control_api_token': remote_control_api_token,
        'cfg_local_ip': ip
    }
    # kvs必须是Dict
    assert isinstance(kvs, dict)
    # 更新设备期望状态文件
    with open(APP_RESOURCES_DATA_PATH + 'iotx_devstat/report_for_iot.json', mode='r+') as f:
        report_devstat_json = json.loads(f.read())
        for (key, value) in kvs.items():
            report_devstat_json['state']['reported'][key] = value
        f.seek(0)
        f.write(json.dumps(report_devstat_json) + '                        ')