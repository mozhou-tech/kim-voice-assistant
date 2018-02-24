# 介绍 

交谈，是我们每天都在做的事，也是最容易习惯的人机交互方式，这是各种音箱大卖的原因之一。"Kim智能语音助理"是一个开源的语音、文本交互方案。同时，通过部署云端服务，使设备具备远程会话能力能力，增加可玩性。

除此之外，Kim的目标是将智能语音助理与智能家居系统无缝结合，我们已经支持著名开源智能家居系统"HomeAssistant"，可以接入小米、博联等主流品牌的智能家居设备。

与阿里云的深度融合，使Kim对云端能力触手可及，让你的私人语音助理更加智能，更易扩展，充满魅力。


[![GitHub issues](https://img.shields.io/github/issues/tenstone/kim-voice-assistant-iot-client.svg)](https://github.com/tenstone/kim-voice-assistant-iot-client/issues)
[![Python3.6](https://img.shields.io/badge/python3.6-green-brightgreen.svg)](https://www.python.org)
[![GitHub license](https://img.shields.io/github/license/tenstone/kim-voice-assistant-iot-client.svg)](https://github.com/tenstone/kim-voice-assistant-iot-client/blob/master/LICENSE)


## 主要特性

1. 基于阿里云构建
1. Docker化快速安装部署
1. 优化中文语义仲裁算法（KSM），精准理解中文语义
2. 可选安装"远程会话服务"
2. 跨平台支持Respberry Pi、macOS、Windows

## 应用场景

### 内置功能

1. 智能家居控制
1. 讲段子，查天气、查快递等
1. 听新闻头条，热门微博
……

### 编写插件，扩展Kim的能力

1. 根据用户意图，请求外部网络接口，完成语音对话交互（或selenium实现Web语音交互）
1. 语音客服机器人
……

你完全可以把Kim作为一个交互入口，去实现更多功能。

## 技术架构

![technical architecture](https://raw.githubusercontent.com/tenstone/kim-voice-assistant-iot-client/master/images/technical_architecture.png)

# 安装使用

## 通过Docker镜像安装

Respbian/Ubuntu/CentOS等有声卡支持（/dev/snd）的设备。

## 直接安装（支持Windows、macOS等平台）

1. 通过

# TODO

1. 支持Docker镜像安装（语音模式仅支持基于Linux Kernel的平台）

# 鸣谢

1. 感谢阿里云提供技术支持
1. 感谢阿里云[天池大赛官方](https://tianchi.aliyun.com/)
1. 感谢[The Jasper Project](http://jasperproject.github.io/)




