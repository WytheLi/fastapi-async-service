from datetime import datetime

import pytz
from zoneinfo import ZoneInfo  # Python 3.9+ 可以使用 zoneinfo 代替 pytz


def convert_to_user_timezone(utc_time: datetime, timezone: str) -> datetime:
    """ 将UTC时间转换为用户指定的时区 """
    utc_time = utc_time.replace(tzinfo=pytz.UTC)
    user_timezone = pytz.timezone(timezone)
    local_time = utc_time.astimezone(user_timezone)
    return local_time
