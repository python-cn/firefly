# coding=utf-8
from __future__ import absolute_import
from datetime import datetime

from dateutil import tz as dateutil_tz
import arrow


def _arrow(d):
    if not d:
        d = arrow.utcnow()

    return arrow.get(d)


def _format(unit, sign):
    return '{0}{1}'.format(sign, unit)


def timesince(d=None, locale='en_us'):
    past = _arrow(d)
    return past.humanize(None, locale)


def short_timesince(d=None, other=None, locale='en_us'):
    past = _arrow(d)
    locale = arrow.locales.get_locale(locale)
    if other is None:
        utc = datetime.utcnow().replace(tzinfo=dateutil_tz.tzutc())
        dt = utc.astimezone(past._datetime.tzinfo)
    elif isinstance(other, arrow.Arrow):
        dt = d._datetime
    elif isinstance(other, datetime):
        if d.tzinfo is None:
            dt = d.replace(tzinfo=past._datetime.tzinfo)
        else:
            dt = d.astimezone(past._datetime.tzinfo)
    else:
        raise TypeError()

    delta = int(arrow.util.total_seconds(past._datetime - dt))
    sign = 1 if delta < 0 else -1
    diff = abs(delta)
    delta = diff

    if diff < 10:
        return 'now'
    elif diff < 45:
        return _format('s', sign)
    elif diff < 90:
        return _format('m', sign)
    elif diff < 2700:
        minutes = sign * int(max(delta / 60, 2))
        return _format('m', minutes)
    elif diff < 5400:
        return _format('h', sign)
    elif diff < 79200:
        hours = sign * int(max(delta / 3600, 2))
        return _format('h', hours)
    elif diff < 129600:
        return _format('d', sign)
    elif diff < 2160000:
        days = sign * int(max(delta / 86400, 2))
        return _format('d', days)
    elif diff < 29808000:
        return past._datetime.strftime('%b %d')
    else:
        return past._datetime.strftime("%b '%y")
