# 小云 
基于阿里云服务的开源智能音箱
灵感来自jasper-client



# 依赖
## Python依赖
二级依赖是需要在操作系统中安装的软件，如果你使用MacOS可以执行：
```
brew install xxx  
```
##安装snowboy
编译安装ATLAS：
https://ncu.dl.sourceforge.net/project/math-atlas/Stable/3.10.3/atlas3.10.3.tar.bz2

```
pip3 install python-pyaudio python3-pyaudio sox
sudo apt-get install libatlas-base-dev
git clone https://github.com/swig/swig.git
pip install pyaudio
```
##安装rpi.gpio
```
sudo apt-get install python3-rpi.gpio
```

| 依赖 | 描述 | 二级依赖 | 实现功能 |  
|-----|----|----|----|
| pyAudio | | 依赖portAudio | 音频播放 | 


# 感谢
1. [Jasper](http://jasperproject.github.io/)






