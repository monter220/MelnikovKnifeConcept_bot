from datetime import datetime

import pytz

from core.config import TIMEZONE


def current_time_with_timezone():
    timezone = pytz.timezone(TIMEZONE)
    return datetime.now(timezone)


def make_datetime_timezone_aware(dt, timezone=TIMEZONE):
    """Преобразуем offset-naive datetime в offset-aware."""
    tz = pytz.timezone(timezone)
    return tz.localize(dt)
