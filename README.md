# 介绍 

交谈，是我们每天都在做的事，也是最容易习惯的人机交互方式，这是各种音箱大卖的原因之一。

"Kim智能语音助理"是一个开源的语音、文本交互方案，由客户端、远程会话端两部分构成。通过部署云端服务，使远端APP控制和API接入能力，增加可玩性。除此之外，Kim的目标是将智能语音助理与智能家居系统无缝结合，我们已经支持著名开源智能家居系统"HomeAssistant"，支持小米、博联等主流品牌的智能家居设备。

Kim与阿里云的深度融合，使设备对云端能力触手可及，让你的私人语音助理更加"智能化"，更容易实现功能扩展，充满魅力。


[![GitHub issues](https://img.shields.io/github/issues/tenstone/kim-voice-assistant-iot-client.svg)](https://github.com/tenstone/kim-voice-assistant-iot-client/issues)
[![Python3.6](https://img.shields.io/badge/python3.6-green-brightgreen.svg)](https://www.python.org)
[![GitHub license](https://img.shields.io/github/license/tenstone/kim-voice-assistant-iot-client.svg)](https://github.com/tenstone/kim-voice-assistant-iot-client/blob/master/LICENSE)


## 特性

1. 基于Alibaba Cloud Services构建
1. 通过Docker管理运行环境，支持快速安装部署
1. 优化中文语义仲裁算法，更加精准的理解中文语义
2. 可选安装Web和OpenAPI控制方案，提供丰富的设备的控制方式
2. 支持树莓派（或其他物联网硬件）、macOS、PC，跨平台安装运行

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




