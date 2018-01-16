# -*- coding: utf-8-*-
import datetime as dt
import pytz
from src.plugins import is_all_word_segment_in_text
WORDS = ["时间", "几点", '周几', '星期几', '几号', '日期']

week_map = ['日', '一', '二', '三', '四', '五', '六']


def handle(text, mic, profile, iot_client=None):
    """
        Reports the current time based on the user's timezone.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
        wxBot -- wechat robot
    """
    tz = pytz.timezone(profile.timezone)
    now = dt.datetime.now(tz=tz)
    if is_all_word_segment_in_text(['时间', '几点'], text):
        mic.say(u"现在时间，%s " % now.strftime("%p%I时%M分").replace('AM', '上午').replace('PM', '下午'))
    else:
        mic.say(u"今天是，" + now.strftime("%Y年%m月%d日") + '，星期'+week_map[int(now.strftime('%w'))])


def is_valid(text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return is_all_word_segment_in_text(WORDS, text)
