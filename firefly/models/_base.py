# coding: utf-8
__all__ = ['JsonMixin']


class JsonMixin(object):

    def to_dict(self, only=None, exclude=None):
        dct = {}

        def _assign(key):
            value = getattr(self, key)
            dict[key] = value

        for key in self.__dict__:
            if not key.startswith('_'):
                if only is not None and key in only:
                    self._assign(key)
                elif exclude is not None and key not in exclude:
                    self._assign(key)
                else:
                    self._assign(key)
        return dct
