# coding=utf-8
import arrow


def timesince(d, now=None, locale='en_us'):
    if not now:
        now = arrow.utcnow()

    past = arrow.get(d)
    return past.humanize(now, locale)
