import json
from urllib2 import urlopen, HTTPError
import fanart

class FanartError(Exception):
    def __str__(self):
        return ', '.join(map(str, self.args))

    def __repr__(self):
        name = self.__class__.__name__
        return '%s%r' % (name, self.args)


class ResponseFanartError(FanartError):
    pass


class RequestFanartError(FanartError):
    pass


class Response(dict):
    def __init__(self, response, **kwargs):
        super(Response, self).__init__(**kwargs)
        try:
            self.update(json.loads(response))
        except (ValueError, KeyError, TypeError):
            raise ResponseFanartError(response)


class Request(object):
    response_cls = Response
    def __init__(self, apikey, id, ws, type=None, sort=None, limit=None):
        self._apikey = apikey
        self._id = id
        self._ws = ws
        if self._ws not in fanart.WS_LIST:
            raise RequestFanartError ('Not allowed ws: %s [%s]' % (self._ws, ', '.join(fanart.WS_LIST)))
        self._type = type or fanart.TYPE.ALL
        if self._type not in fanart.TYPE_LIST:
            raise RequestFanartError ('Not allowed type: %s [%s]' % (self._type, ', '.join(fanart.TYPE_LIST)))
        self._sort = sort or fanart.SORT.POPULAR
        if self._sort not in fanart.SORT_LIST:
            raise RequestFanartError ('Not allowed sort: %s [%s]' % (self._sort, ', '.join(fanart.SORT_LIST)))
        self._limit = limit or fanart.LIMIT.ALL
        if self._limit not in fanart.SORT_LIST:
            raise RequestFanartError ('Not allowed limit: %s [%s]' % (self._limit, ', '.join(fanart.LIMIT_LIST)))
        self._response = None

    def __str__(self):
        return '/'.join(map(str,[
            fanart.BASEURL,
            self._ws,
            self._apikey,
            self._id,
            fanart.FORMAT.JSON,
            self._type,
            self._sort,
            self._limit,])
        )

    @property
    def response(self):
        if not self._response:
            try:
                response = urlopen(str(self))
            except HTTPError as e:
                response = e
            self._response = self.response_cls(response.read())
        return self._response
