FROM resin/raspberry-pi-python:3.6-slim
LABEL author="tenstone"

ENV SNOWBOY_GIT_URL="https://github.com/Kitt-AI/snowboy.git" SWIG_GIT_URL="https://github.com/swig/swig.git"

RUN echo "deb-src http://mirrors.aliyun.com/raspbian/raspbian/ jessie main contrib non-free rpi" > /etc/apt/sources.list.d/raspi.list \
    &&echo "deb http://mirrors.aliyun.com/raspbian/raspbian/ jessie main contrib non-free rpi" > /etc/apt/sources.list

RUN apt-get update && apt-get -y install sox swig3.0 python-pyaudio python3-pyaudio libatlas-base-dev libportaudio-dev

WORKDIR /root/

RUN curl https://s3-us-west-2.amazonaws.com/snowboy/snowboy-releases/rpi-arm-raspbian-8.0-1.2.0.tar.bz2 \
  | tar -xjC /root/
RUN mv /root/rpi-arm-raspbian-8.0-1.2.0 /root/service

COPY src/* /root/service/

RUN pip install -r /root/service/requirements.txt
COPY walle.pmdl /root/walle.pmdl
COPY asoundrc /root/.asoundrc


CMD [ "python", "/root/service/main.py", "/root/walle.pmdl"]