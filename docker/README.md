
# docker 镜像

https://hub.docker.com/r/mosch/raspberry-pi-snowboy/
https://hub.docker.com/r/resin/rpi-raspbian/'

# 构建

docker build -t --no-cache kimserver kim-server/.



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


