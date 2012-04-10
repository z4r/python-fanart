from fanart.utils import Immutable
from fanart.items import LeafItem, ResourceItem, CollectableItem
import fanart

class BackgroundItem(LeafItem):
    KEY = fanart.TYPE.MUSIC.BACKGROUND


class CoverItem(LeafItem):
    KEY = fanart.TYPE.MUSIC.COVER


class LogoItem(LeafItem):
    KEY = fanart.TYPE.MUSIC.LOGO


class ArtItem(LeafItem):
    KEY =  fanart.TYPE.MUSIC.ART

    @Immutable.mutablemethod
    def __init__(self, id, url, likes, disc, size):
        super(ArtItem, self).__init__(id, url, likes)
        self.disc = int(disc)
        self.size = int(size)


class Artist(ResourceItem):
    WS = fanart.WS.MUSIC

    @Immutable.mutablemethod
    def __init__(self, name, mbid, albums, backgrounds, logos):
        self.name = name
        self.mbid = mbid
        self.albums = albums
        self.backgrounds = backgrounds
        self.logos = logos

    @classmethod
    def from_dict(cls, map):
        assert len(map) == 1, 'Bad Format Map'
        name, map = map.items()[0]
        return cls(
            name = name,
            mbid = map['mbid_id'],
            albums = Album.collection_from_dict(map.get('albums', {})),
            backgrounds = BackgroundItem.extract(map),
            logos = LogoItem.extract(map),
        )


class Album(CollectableItem):

    @Immutable.mutablemethod
    def __init__(self, mbid, covers, arts):
        self.mbid = mbid
        self.covers = covers
        self.arts = arts

    @classmethod
    def from_dict(cls, key, map):
        return cls(
            mbid = key,
            covers = CoverItem.extract(map),
            arts = ArtItem.extract(map),
        )