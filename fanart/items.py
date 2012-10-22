import os
import urllib2
from fanart.core import Request


class Immutable(object):
    _mutable = False

    def __setattr__(self, name, value):
        if self._mutable or name == '_mutable':
            super(Immutable, self).__setattr__(name, value)
        else:
            raise TypeError("Can't modify immutable instance")

    def __delattr__(self, name):
        if self._mutable:
            super(Immutable, self).__delattr__(name)
        else:
            raise TypeError("Can't modify immutable instance")

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(repr(self))

    def __repr__(self):
        return '%s(%s)' % (
            self.__class__.__name__,
            ', '.join(['{0}={1}'.format(k, repr(v)) for k, v in self])
        )

    def __iter__(self):
        l = self.__dict__.keys()
        l.sort()
        for k in l:
            if not k.startswith('_'):
                yield k, getattr(self, k)

    @staticmethod
    def mutablemethod(f):
        def func(self, *args, **kwargs):
            if isinstance(self, Immutable):
                old_mutable = self._mutable
                self._mutable = True
                res = f(self, *args, **kwargs)
                self._mutable = old_mutable
            else:
                res = f(self, *args, **kwargs)
            return res
        return func


class LeafItem(Immutable):
    KEY = NotImplemented

    @Immutable.mutablemethod
    def __init__(self, id, url, likes):
        self.id = int(id)
        self.url = url
        self.likes = int(likes)

    @classmethod
    def from_dict(cls, resource):
        return cls(**dict([(str(k), v) for k, v in resource.iteritems()]))

    @classmethod
    def extract(cls, resource):
        return [cls.from_dict(i) for i in resource.get(cls.KEY, {})]

    def __str__(self):
        return self.url

    def write(self, path='.'):
        _, ext = os.path.splitext(self.url)
        filepath = os.path.join(path, '%d%s' % (self.id, ext))
        response = urllib2.urlopen(self.url)
        with open(filepath, 'wb') as fp:
            fp.write(response.read())


class ResourceItem(Immutable):
    WS = NotImplemented
    request_cls = Request

    @classmethod
    def from_dict(cls, map):
        raise NotImplementedError

    @classmethod
    def get(cls, id):
        map = cls.request_cls(
            apikey=os.environ.get('FANART_APIKEY'),
            id=id,
            ws=cls.WS
        ).response
        return cls.from_dict(map)


class CollectableItem(Immutable):
    @classmethod
    def from_dict(cls, key, map):
        raise NotImplementedError

    @classmethod
    def collection_from_dict(cls, map):
        return [cls.from_dict(k, v) for k, v in map.iteritems()]
