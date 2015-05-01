# coding=utf-8
from .consts import STATUS_MAPS, UNKNOWN


def generate_status_fields(status_code, message=None):
    if status_code in STATUS_MAPS:
        if message is None:
            message = STATUS_MAPS[status_code]
    else:
        status_code = UNKNOWN
        message = STATUS_MAPS[UNKNOWN]
    return {'status': status_code, 'message': message}
