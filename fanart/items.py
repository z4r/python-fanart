import os
from fanart.core import Request
from fanart.utils import Immutable

class BaseItem(Immutable):
    def __iter__(self):
        iterdict = self.__dict__.iteritems()
        return ((k, v) for k,v in iterdict if not k.startswith('_'))

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, ', '.join(
            ['{0}={1}'.format(k,repr(v)) for k,v in sorted(self)])
        )

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return hash(self) == hash(other)


class LeafItem(BaseItem):
    KEY = NotImplemented

    @Immutable.mutablemethod
    def __init__(self, id, url, likes):
        self.id = int(id)
        self.url = url
        self.likes = int(likes)

    @classmethod
    def from_dict(cls, map):
        return cls(**dict([(str(k), v) for k, v in map.iteritems()]))

    @classmethod
    def extract(cls, map):
        return [cls.from_dict(i) for i in map.get(cls.KEY, {})]

    def __str__(self):
        return self.url


class ResourceItem(BaseItem):
    WS = NotImplemented
    request_cls = Request

    @classmethod
    def from_dict(cls, map):
        raise NotImplementedError

    @classmethod
    def get(cls, id):
        map = cls.request_cls(
            apikey = os.environ.get('FANART_APIKEY'),
            id = id,
            ws = cls.WS
        ).response
        return cls.from_dict(map)


class CollectableItem(BaseItem):
    @classmethod
    def from_dict(cls, key, map):
        raise NotImplementedError

    @classmethod
    def collection_from_dict(cls, map):
        return [cls.from_dict(k, v) for k, v in map.iteritems()]