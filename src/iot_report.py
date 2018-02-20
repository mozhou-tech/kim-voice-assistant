# -*- coding: utf-8-*-
import json
from config.path import APP_RESOURCES_DATA_PATH
from config.profile import myname,timezone,city,\
    remote_control_service_enable,remote_control_password
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
    kvs = {
        'myname': myname,
        'timezone': timezone,
        'city': city,
        'remote_control_service_enable': remote_control_service_enable,
        'remote_control_password': remote_control_password
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