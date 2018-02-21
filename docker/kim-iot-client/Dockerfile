FROM resin/rpi-raspbian

LABEL author=tenstone
ENV PROJECT_DIR="kim-voice-assistant-iot-client" PROJECT_GIT_PATH="https://github.com/tenstone/kim-voice-assistant-iot-client.git"
#  docker run --device=/dev/snd:/dev/snd  |for linux
WORKDIR /usr/src/app

COPY . .

    # 配置国内镜像，安装一些包
RUN echo "deb http://mirrors.aliyun.com/raspbian/raspbian/ jessie main non-free contrib\ndeb-src http://mirrors.aliyun.com/raspbian/raspbian/ jessie main non-free contrib" >> /etc/apt/sources.list && \
    mkdir ~/.pip/ && \
    echo "[global]\nindex-url = http://mirrors.aliyun.com/pypi/simple/\n\n[install]\ntrusted-host=mirrors.aliyun.com" >> ~/.pip/pip.conf

#RUN apt-get install git gcc g++ make libffi-dev openssl-dev


