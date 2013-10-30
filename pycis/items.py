""" This module represent the base classes for wrappers sending information to interfaces

classes:
    Stream
    Media

example subclasses:
    Film
    TvShow
    Song
"""


class Stream(object):

    """ Stream objects contains info to extracting downloading stream """

    def __init__(self, id, host, url):
        self.id = id
        self.host = host
        self.url = url


class Media(object):

    """ Holds info about a media object it may be a film, tvshow, episode, music

    If has_children is true it means that this media contain children media 
    to be fetched before getting streams in a group. Tvshows are a good example 
    as they contain multiple children episodes.
    """

    def __init__(self, title, url, has_children=False):
        self.title = title
        self.url = url
        self.has_children = has_children

        self.description = None
        self.rating = None
        self.genres = []
        self.year = None
        self.thumbnail = None

    @property
    def code(self):
        """ return code to be used on the interface instead of its enumeration index """
        return None

    @property
    def extra_info(self):
        """ return extra info to be printed on the interface """
        return None

    def __str__(self):
        class_name = self.__class__.__name__
        fstr = u'{0}(title="{1.title!s}", url="{1.url!s}", has_children={1.has_children!s})'

        return fstr.format(class_name, self)


class Film(Media):

    def __init__(self, title, url, has_children=False, actors=None, directors=None):
        super(Film, self).__init__(title, url, has_children)

        self.actors = actors if actors else []
        self.directors = directors if directors else []


class TvShow(Media):

    def __init__(self, title, url, has_children=False, season_num=None, episode=None):
        super(TvShow, self).__init__(title, url, has_children)

        self.season_num = season_num
        self.episode_num = episode_num

    @property
    def code(self):
        if self.season_num and self.episode_num:
            return u's{0:02d}e{1:02d}'.format(self.season_num, self.episode_num)


class Song(Media):

    def __init__(self, title, url, artist=None, album=None, composer=None, has_children=False):
        super(Song, self).__init__(title, url, has_children)

        self.artist = artist
        self.album = album
        self.composer = composer
