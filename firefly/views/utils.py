# coding=utf-8
import pytz
import datetime


TIMESINCE_CHUNKS = (
    (60 * 60 * 24 * 365, '%d years'),
    (60 * 60 * 24 * 30, '%d months'),
    (60 * 60 * 24 * 7, '%d weeks'),
    (60 * 60 * 24, '%d days'),
    (60 * 60, '%d hours'),
    (60, '%d minutes')
)


def is_aware(value):
    return value.tzinfo is not None and value.tzinfo.utcoffset(value) \
        is not None


def timesince(d, now=None, reversed=False):
    # Convert datetime.date to datetime.datetime for comparison.
    if not isinstance(d, datetime.datetime):
        d = datetime.datetime(d.year, d.month, d.day)
    if now and not isinstance(now, datetime.datetime):
        now = datetime.datetime(now.year, now.month, now.day)

    if not now:
        now = datetime.datetime.now(pytz.utc if is_aware(d) else None)

    delta = (d - now) if reversed else (now - d)
    # ignore microseconds
    since = delta.days * 24 * 60 * 60 + delta.seconds
    if since <= 0:
        # d is in the future compared to now, stop processing.
        return '0 minutes'
    for i, (seconds, name) in enumerate(TIMESINCE_CHUNKS):
        count = since // seconds
        if count != 0:
            break
    result = name % count
    if i + 1 < len(TIMESINCE_CHUNKS):
        # Now get the second item
        seconds2, name2 = TIMESINCE_CHUNKS[i + 1]
        count2 = (since - (seconds * count)) // seconds2
        if count2 != 0:
            result += ', ' + name2 % count2
    return result
