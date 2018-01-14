# 小云 
基于阿里云服务的开源智能音箱
灵感来自jasper-client



# 依赖
## Python依赖
二级依赖是需要在操作系统中安装的软件，如果你使用MacOS可以执行：
```
brew install xxx  
```
portaudio
##安装snowboy
编译安装ATLAS：
https://ncu.dl.sourceforge.net/project/math-atlas/Stable/3.10.3/atlas3.10.3.tar.bz2

```
pip3 install python-pyaudio python3-pyaudio sox
sudo apt-get install libatlas-base-dev
git clone https://github.com/swig/swig.git
pip install pyaudio
sudo apt-get install alsa-tools alsa-utils
sudo apt-get install libblas3 libblas-dev libatlas-dev libatlas-base-dev
sudo apt-get install python-cffi
sudo apt-get install libffi-dev
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev
sudo apt-get install sox
sudo pip3 install RPi.GPIO
sudo pip3 install RPIO
```
如果出现错误，请参考：https://github.com/Kitt-AI/snowboy/issues/94
##安装rpi.gpio
```
sudo apt-get install python3-rpi.gpio
sudo systemctl enable pigpiod
```

| 依赖 | 描述 | 二级依赖 | 实现功能 |  
|-----|----|----|----|
| pyAudio | | 依赖portAudio | 音频播放 | 


## 配置
到 [Snowboy](https://snowboy.kitt.ai/dashboard) 创建你自己的热词模型，下载文件放到
config/hotword_models目录中。
alsamixer  选择声卡
### GPIO针脚对照表
| 模块 | 针脚 | 功能 |
|----|----|----|
| LED | GPIO9 | LED-RED | 
| LED | GPIO10 | LED-GREEN | 
| LED | GPIO11 | LED-BLUE |
| 步进电机 | GPIO17 | IN1 |
| 步进电机 | GPIO18 | IN2 |
| 步进电机 | GPIO27 | IN3 |
| 步进电机 | GPIO22 | IN4 |
| 光敏传感器 | GPIO4 | DO |
| 红外传感器 | GPIO3 | DO |


## 云计算端部署
iot和函数计算均在华东2区开通

# 感谢
1. [Jasper](http://jasperproject.github.io/)






