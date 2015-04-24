# coding: utf-8
__all__ = ['dict_filter']


def dict_filter(source, only=None, exclude=None):
    # source is a normal dict
    dct = {}

    def _assign(key):
        value = getattr(source, key)
        dct[key] = value

    for key in source.__dict__:
        if not key.startswith('_'):
            if only is not None:
                if key in only:
                    _assign(key)
            elif exclude is not None:
                if key not in exclude:
                    _assign(key)
            else:
                _assign(key)
    return dct
