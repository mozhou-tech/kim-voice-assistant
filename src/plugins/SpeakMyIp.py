# -*- coding: utf-8-*-
import re,requests
from src.plugins import is_all_word_segment_in_text, plugin_output
import socket

WORDS = ["IP地址", "IP", "网络地址", 'ip', 'ip地址']


def __get_internet_ip():

    url = "http://cn.bing.com/search?q=ip&go=%E6%8F%90%E4%BA%A4&qs=n&form=QBLH&pq=ip&sc=8-2&sp=-1&sk=&cvid=14b93b305cdc4183875411c3d9edf938"
    html = requests.get(url)
    # print html
    html_re = re.compile(r'本机 ip: (.+?) 上海市 联通', re.DOTALL)
    for x in html_re.findall(html.content.decode('utf8')):
        return x


def __get_host_ip():
    """
    获取本机IP地址
    :return:
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def handle(text, mic, profile, iot_client=None, chatbot=None):
    """
    插件入口函数
    :param text:
    :param mic:
    :param profile:
    :param iot_client:
    :param chatbot:
    :return:
    """
    robot_says = "我的I P地址是 "+__get_host_ip()
    plugin_output(text, mic, robot_says)


def is_valid(text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return is_all_word_segment_in_text(WORDS, text)
