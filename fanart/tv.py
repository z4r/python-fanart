import fanart
from fanart.items import LeafItem, Immutable, ResourceItem

class TvItem(LeafItem):

    @Immutable.mutablemethod
    def __init__(self, id, url, likes, lang):
        super(TvItem, self).__init__(id, url, likes)
        self.language = lang


class CharacterItem(TvItem):
    KEY = fanart.TYPE.TV.CHARACTER


class ArtItem(TvItem):
    KEY = fanart.TYPE.TV.ART


class LogoItem(TvItem):
    KEY = fanart.TYPE.TV.LOGO


class SeasonItem(TvItem):

    @Immutable.mutablemethod
    def __init__(self, id, url, likes, lang, season):
        super(SeasonItem, self).__init__(id, url, likes, lang)
        self.season = int(season)


class ThumbItem(TvItem):
    KEY = fanart.TYPE.TV.THUMB


class TvShow(ResourceItem):
    WS = fanart.WS.TV

    @Immutable.mutablemethod
    def __init__(self, name, tvdbid, characters, arts, logos, seasons, thumbs):
        self.name = name
        self.tvdbid = tvdbid
        self.characters = characters
        self.arts = arts
        self.logos = logos
        self.seasons = seasons
        self.thumbs = thumbs

    @classmethod
    def from_dict(cls, resource):
        assert len(resource) == 1, 'Bad Format Map'
        name, resource = resource.items()[0]
        return cls(
            name = name,
            tvdbid = resource['thetvdb_id'],
            characters = CharacterItem.extract(resource),
            arts = ArtItem.extract(resource),
            logos = LogoItem.extract(resource),
            seasons = SeasonItem.extract(resource),
            thumbs = ThumbItem.extract(resource)
        )