# coding=utf-8
from collections import OrderedDict


def generate_status_fields(status_code, message):
    return OrderedDict({'status': status_code, 'message': message})
