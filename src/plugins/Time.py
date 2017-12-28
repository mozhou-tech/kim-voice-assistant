# -*- coding: utf-8-*-
import datetime as dt
import pytz
WORDS = [u"TIME", u"SHIJIAN", u"JIDIAN"]
SLUG = "time"


def handle(text, mic, profile):
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
    mic.say(u"现在时间，%s " % now.strftime("%m月%d号%p%I时%M分").replace('AM', '上午').replace('PM', '下午'))


def isValid(text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return any(word in text for word in ["时间", "几点"])
