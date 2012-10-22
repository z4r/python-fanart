__author__ = 'Andrea De Marco <24erre@gmail.com>'
__version__ = '0.2'
__classifiers__ = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Software Development :: Libraries',
]
__copyright__ = "2012, %s " % __author__
__license__ = """
   Copyright %s.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either expressed or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
""" % __copyright__

__docformat__ = 'restructuredtext en'

__doc__ = """
:abstract: Python interface to fanart.tv API
:version: %s
:author: %s
:contact: http://z4r.github.com/
:date: 2012-04-04
:copyright: %s
""" % (__version__, __author__, __license__)


def values(obj):
    return [v for k, v in obj.__dict__.iteritems() if not k.startswith('_')]

BASEURL = 'http://fanart.tv/webservice'


class FORMAT(object):
    JSON = 'JSON'
    XML = 'XML'
    PHP = 'PHP'


class WS(object):
    MUSIC = 'artist'
    MOVIE = 'movie'
    TV = 'series'


class TYPE(object):
    ALL = 'all'

    class TV(object):
        ART = 'clearart'
        LOGO = 'clearlogo'
        CHARACTER = 'characterart'
        THUMB = 'tvthumb'
        SEASONTHUMB = 'seasonthumb'
        BACKGROUND = 'showbackground'

    class MUSIC(object):
        DISC = 'cdart'
        LOGO = 'musiclogo'
        BACKGROUND = 'artistbackground'
        COVER = 'albumcover'

    class MOVIE(object):
        ART = 'movieart'
        LOGO = 'movielogo'
        DISC = 'moviedisc'


class SORT(object):
    POPULAR = 1
    NEWEST = 2
    OLDEST = 3


class LIMIT(object):
    ONE = 1
    ALL = 2

FORMAT_LIST = values(FORMAT)
WS_LIST = values(WS)
TYPE_LIST = values(TYPE.MUSIC) + values(TYPE.TV) + values(TYPE.MOVIE) + [TYPE.ALL]
MUSIC_TYPE_LIST = values(TYPE.MUSIC) + [TYPE.ALL]
TV_TYPE_LIST = values(TYPE.TV) + [TYPE.ALL]
MOVIE_TYPE_LIST = values(TYPE.MOVIE) + [TYPE.ALL]
SORT_LIST = values(SORT)
LIMIT_LIST = values(LIMIT)

import logging
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass
logging.getLogger(__name__).addHandler(NullHandler())

LOG_LEVELS = {
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG,
}


def set_logging(level, handler=None):
    if not handler:
        handler = logging.StreamHandler()
    fmt = r'[%(levelname)s] %(message)s'
    handler.setFormatter(logging.Formatter(fmt))
    logger = logging.getLogger(__name__)
    logger.setLevel(LOG_LEVELS.get(level, logging.INFO))
    logger.addHandler(handler)
