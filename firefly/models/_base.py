# coding: utf-8
__all__ = ['JsonMixin']


class JsonMixin(object):

    def to_dict(self, only=None, exclude=None):
        dct = {}

        def _assign(key):
            value = getattr(self, key)
            dct[key] = value

        for key in self._data:
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
