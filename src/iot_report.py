# -*- coding: utf-8-*-
import json,socket,os
from src.config.path import APP_RESOURCES_DATA_PATH ,HOTWORD_MODEL_PATH
from src.config.profile import myname,timezone,city,\
    remote_control_service_enable,remote_control_password,remote_control_api_token,\
    aliyun_tablestore_endpoint, aliyun_tablestore_instance, aliyun_tablestore_table
"""
组织用于报告给Iothub的数据
"""


def __get_host_ip():
    """
    获取本地IP地址
    :return:
    """

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


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

    kvs = {
        'cfg_myname': myname,
        'cfg_timezone': timezone,
        'cfg_city': city,
        'cfg_remote_control_service_enable': remote_control_service_enable,
        'cfg_remote_control_password': remote_control_password,
        'cfg_remote_control_api_token': remote_control_api_token,
        'cfg_local_ip': __get_host_ip(),
        'cfg_hotword_files': ','.join(os.listdir(HOTWORD_MODEL_PATH)),
        'cfg_device_client_version': '1.0',
        'cfg_tablestore_endpoint': aliyun_tablestore_endpoint,
        'cfg_tablestore_instance': aliyun_tablestore_instance,
        'cfg_tablestore_table': aliyun_tablestore_table,

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