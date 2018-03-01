# 介绍 

交谈，是我们每天都在做的事，也是最容易习惯的人机交互方式，这是各种音箱大卖的原因之一。"Kim智能语音助理"是一个开源的语音、文本交互方案。同时，通过部署云端服务，使设备具备远程会话能力能力，增加可玩性。

除此之外，Kim的目标是将智能语音助理与智能家居系统无缝结合，我们已经支持著名开源智能家居系统"HomeAssistant"，可以接入小米、博联等主流品牌的智能家居设备。

与阿里云的深度融合，使Kim对云端能力触手可及，让你的私人语音助理更加智能，更易扩展，充满魅力。

[![Python3.6](https://img.shields.io/badge/python3.6-green-brightgreen.svg)](https://www.python.org)
[![GitHub issues](https://img.shields.io/github/issues/tenstone/kim-voice-assistant.svg)](https://github.com/tenstone/kim-voice-assistant/issues)
[![Shippable](https://img.shields.io/shippable/5444c5ecb904a4b21567b0ff.svg)]()
[![GitHub license](https://img.shields.io/github/license/tenstone/kim-voice-assistant.svg)](https://github.com/tenstone/kim-voice-assistant/blob/master/LICENSE)

## 关联项目

1. [Kim远程会话服务(RemoteTalk)](https://github.com/tenstone/kim-voice-assistant-remotetalk)
1. [Kim插件集](https://github.com/tenstone/kim-voice-assistant-plugins)

## 主要特性

1. 基于阿里云服务构建
1. Docker化快速安装部署
1. 优化中文语义仲裁算法（KSM），精准理解中文语义
2. 可选安装"远程会话服务"
2. 跨平台支持Respberry Pi、macOS、Windows
1. 响应消息可通过[DingTalk机器人](DingTalk机器人)推送到群

## 应用场景

### 内置插件

1. 智能家居控制
1. 讲段子，查天气、查快递等
1. 听新闻头条，热门微博
1. [更多...](https://github.com/tenstone/kim-voice-assistant/wiki/自定义插件)

### 自定义插件，扩展Kim的能力

1. 根据用户意图，请求外部网络接口，完成语音对话交互（或selenium实现Web语音交互）
1. 智能语音客服机器人
1. 你完全可以把Kim作为一个交互入口，通过插件实现丰富的后端功能

参见文章"[自定义插件](https://github.com/tenstone/kim-voice-assistant/wiki/自定义插件)"查看自定义插件的详细介绍。


## 技术架构

Kim基于Python36构建，设备端实现了中文语义仲裁算法和"Kim大脑"，通过大脑理解设备输入；会话日志数据存储、插件、设备在线状态及数据传输等功能基于阿里云服务实现。

![technical architecture](https://raw.githubusercontent.com/tenstone/kim-voice-assistant/master/images/technical_architecture.png)


# 安装使用

## 安装

* [安装设备端](https://github.com/tenstone/kim-voice-assistant/wiki/安装(IotClient))
* [安装远程会话端](https://github.com/tenstone/kim-voice-assistant/wiki/安装(RemoteTalk))

## 配置

* [获取阿里云AccessKey](https://github.com/tenstone/kim-voice-assistant/wiki/获取阿里云AccessKey)
* [配置物联网套件](https://github.com/tenstone/kim-voice-assistant/wiki/配置物联网套件)
* [配置表格存储](https://github.com/tenstone/kim-voice-assistant/wiki/配置表格存储)
* [配置云小蜜聊天机器人](https://github.com/tenstone/kim-voice-assistant/wiki/配置云小蜜聊天机器人)
* [配置DingTalk群机器人](https://github.com/tenstone/kim-voice-assistant/wiki/配置DingTalk群机器人)
* [配置HomeAssistant](https://github.com/tenstone/kim-voice-assistant/wiki/)
* [配置HA与阿里智能](https://github.com/tenstone/kim-voice-assistant/wiki/)
* [配置HA与小米智能](https://github.com/tenstone/kim-voice-assistant/wiki/配置HA与小米智能)

# 技术支持

## 钉钉交流群

用钉钉扫描下方二维码，入群交流。

![钉钉群](https://raw.githubusercontent.com/tenstone/kim-voice-assistant/master/images/dingdingqun.jpg)

# TODO

1. 插件被修改时，Brain自动重载插件（已实现）
1. 支持HomeAssistant
1. 支持Docker镜像安装（语音模式仅支持基于Linux Kernel的平台）

# 鸣谢

1. 感谢阿里云提供技术支持
1. 感谢阿里云[天池大赛](https://tianchi.aliyun.com/)官方
1. 感谢[The Jasper Project](http://jasperproject.github.io/)和[DingDang](https://github.com/wzpan/dingdang-robot)的开发者，他们启发了我的灵感





