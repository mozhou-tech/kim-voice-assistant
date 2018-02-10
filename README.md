# 介绍 

Kim Voice Assistant是基于阿里云服务的开源智能音箱，灵感来自外国友人的开源项目[jasper-client](http://jasperproject.github.io/)。Kim在安装、本土化、控制方式等方面提出了不少改进方案，使得项目更容易上手，可玩性也有不少提升。项目中的不足，欢迎批评指点。

## 特性

1. 基于Alibaba Cloud优秀的云端服务构建
1. 通过Docker管理运行环境，支持快速部署
1. 优化中文语义仲裁算法，更加精准的理解中文语义
2. 增加Web控制和OpenAPI的支持，提供丰富的设备的控制方式
2. 支持MQTT协议，对IoT设备提供控制方案

## 组成

| 名称 | 描述 | 链接 |
|----|----|----|
| Kim Voice Assistant Dock | Kim服务运行Docker构建项目（设备端和服务端）  | [Dock](https://github.com/tenstone/kim-voice-assistant-dock) |
| Kim Voice Assistant Iot Client | Kim设备端项目 | [Client](https://github.com/tenstone/kim-voice-assistant-iot-client) |
| Kim Voice Assistant Server | Kim服务器端项目 | [Server](https://github.com/tenstone/kim-voice-assistant-server) |

# 安装

通过Dockerfile构建镜像







