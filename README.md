# Introduction
Kim, is a complete smart home solution. Conversation is what we do every day, so it is one of the most acceptable ways of human-computer interaction. "Kim Intelligent Voice Assistant" provides an open source voice and text interactive solution. At the same time, Kim uses cloud services to enable the device to have remote conversation capabilities and increase playability. Kim has supported the well-known open source smart home system "HomeAssistant", which can access smart home devices from mainstream brands such as Xiaomi and Bolian. The Yunqi community introduced Kim.

The deep integration of Kim and Alibaba Cloud makes Kim's cloud capabilities within reach, making your personal voice assistant smarter, easier to expand, and full of charm.

[![Python3.6](https://img.shields.io/badge/python3.6-green-brightgreen.svg)](https://www.python.org)
[![GitHub issues](https://img.shields.io/github/issues/tenstone/kim-voice-assistant.svg)](https://github.com/tenstone/kim-voice-assistant/issues)
[![Shippable](https://img.shields.io/shippable/5444c5ecb904a4b21567b0ff.svg)]()
[![GitHub license](https://img.shields.io/github/license/tenstone/kim-voice-assistant.svg)](https://github.com/tenstone/kim-voice-assistant/blob/master/LICENSE)

## Associated projects

1. [Kim Remote Talk Service (RemoteTalk)](https://github.com/tenstone/kim-voice-assistant-remotetalk)
1. [Kim Plugin Collection](https://github.com/tenstone/kim-voice-assistant-plugins)

## Main features

1. Built on Alibaba Cloud Service
1. Dockerized rapid installation and deployment
1. Optimize the Chinese semantic arbitration algorithm (KSM) to accurately understand Chinese semantics
2. Optional installation of "Remote Session Service"
2. Cross-platform support for Respberry Pi, macOS, Windows
1. The response message can be pushed to the group via [DingTalk Robot] (DingTalk Robot)

## Application scenario

### Built-in plugins

1. Smart home control
1. Tell stories, check weather, check express delivery, etc.
1. Listen to news headlines, popular Weibo
1. [More...](https://github.com/tenstone/kim-voice-assistant/wiki/Custom Plugin)

### Custom plugins to extend Kim's capabilities

1. According to the user's intention, request an external network interface to complete the voice dialogue interaction (or selenium to achieve Web voice interaction)
1. Intelligent voice customer service robot
1. You can use Kim as an interactive portal to achieve rich back-end functions through plugins

See the article "[Custom Plugin](https://github.com/tenstone/kim-voice-assistant/wiki/Custom Plugin)" for a detailed introduction of custom plugins.

## Technical Architecture

Kim is based on Python36. The device implements the Chinese semantic arbitration algorithm and the "Kim brain" to understand device input through the brain; functions such as session log data storage, plug-ins, device online status and data transmission are implemented based on Alibaba Cloud services.

# Installation & Configuration

## installation method

* [Install device side](https://github.com/tenstone/kim-voice-assistant/wiki/Install(IotClient))
* [Install the remote conversation terminal](https://github.com/tenstone/kim-voice-assistant/wiki/Install(RemoteTalk))

## Configuration steps

* [Get Alibaba Cloud AccessKey](https://github.com/tenstone/kim-voice-assistant/wiki/Get Alibaba Cloud AccessKey)
* [Configure IoT Kit](https://github.com/tenstone/kim-voice-assistant/wiki/Configure IoT Kit)
* [Configure Table Storage](https://github.com/tenstone/kim-voice-assistant/wiki/Configure Table Storage)
* [Configure Yunxiaomi Chatbot](https://github.com/tenstone/kim-voice-assistant/wiki/Configure Yunxiaomi Chatbot)
* [Configure DingTalk Group Robot](https://github.com/tenstone/kim-voice-assistant/wiki/Configure DingTalk Group Robot)
* [Configure HomeAssistant](https://github.com/tenstone/kim-voice-assistant/wiki/)
* [Configure HA and Ali Intelligence](https://github.com/tenstone/kim-voice-assistant/wiki/)
* [Configure HA and Xiaomi Smart](https://github.com/tenstone/kim-voice-assistant/wiki/Configure HA and Xiaomi Smart)

# Technical Support

## Dingding exchange group

Scan the QR code below with Dingding to enter the group and communicate.

![Dingdingqun](https://raw.githubusercontent.com/tenstone/kim-voice-assistant/master/images/dingdingqun.jpg)

# TODO

1. ~~ When the plugin is modified, Kim Brain will automatically reload the plugin (implemented)~~
1. Support HomeAssistant
1. Support Docker image installation (voice mode only supports Linux Kernel-based platforms)

# Thanks

1. Thanks to [supermei](https://github.com/supermei) for participating in the development of "remote conversation terminal" to realize remote control of IOT devices through web pages
1. Thanks to Alibaba Cloud for technical support
1. Thanks to the developers of [The Jasper Project](http://jasperproject.github.io/) and [DingDang](https://github.com/wzpan/dingdang-robot), they inspired me
