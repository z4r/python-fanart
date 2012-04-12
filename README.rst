=================================
Python interface to fanart.tv API
=================================

This package provides a module to interface with the `fanart.tv`_ API.

.. contents::
    :local:

.. _installation:

Installation
============
Using pip::

    $ pip install git+https://github.com/z4r/python-fanart

.. _summary:

FANART API Summary
==================

Low Level
---------

::

    from fanart.core import Request
    import fanart
    request = Request(
        apikey = '<YOURAPIKEY>',
        id = '24e1b53c-3085-4581-8472-0b0088d2508c',
        ws = fanart.WS.MUSIC,
        type = fanart.TYPE.ALL,
        sort = fanart.SORT.POPULAR,
        limit = fanart.LIMIT.ALL,
    )
    print request.response


Music
-----

::

    import os
    os.environ.setdefault('FANART_APIKEY', '<YOURAPIKEY>')

    from fanart.music import Artist

    artist = Artist.get(id = '24e1b53c-3085-4581-8472-0b0088d2508c')
    print artist.name
    print artist.mbid
    for album in artist.albums:
        for cover in album.covers:
            print 'Saving: %s' % cover
            cover.write()

Movie
-----

::

    import os
    os.environ.setdefault('FANART_APIKEY', '<YOURAPIKEY>')

    from fanart.movie import Movie

    movie = Movie.get(id = '70160')


TV Shows
--------

::

    import os
    os.environ.setdefault('FANART_APIKEY', '<YOURAPIKEY>')

    from fanart.tv import TvShow

    tvshow = TvShow.get(id = '80379')

.. _license:

License
=======

This software is licensed under the ``Apache License 2.0``. See the ``LICENSE``
file in the top distribution directory for the full license text.

.. _references:

References
==========
* `fanart.tv`_

.. _fanart.tv: http://fanart.tv/
