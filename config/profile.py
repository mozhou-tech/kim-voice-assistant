# -*- coding: utf-8-*-
import config
yaml_settings = config.load_yaml_settings()
"""
保存用户信息
"""
myname = yaml_settings['profile']['myname']
city = yaml_settings['profile']['city']   # 请包含"市"、"区"字样，例如：南京市、建邺区
timezone = yaml_settings['profile']['timezone']

"""
子账号需要IOT和语音权限
"""
ak_id = yaml_settings['aliyun']['ak_id']
ak_secret = yaml_settings['aliyun']['ak_secret']
ali_appcode = yaml_settings['aliyun']['api_market']['appcode']

"""
阿里云函数计算服务
https://fc.console.aliyun.com/overview/cn-shanghai
"""
aliyun_fc_endpoint = 'http://1435638266713387.cn-shanghai.fc.aliyuncs.com'
aliyun_fc_service_name = 'xiaoyun_fc_service'

"""
远端控制服务
"""
remote_control_service_enable = yaml_settings['remote_control_service']['enable']
remote_control_service_endpoint = yaml_settings['remote_control_service']['endpoint']

