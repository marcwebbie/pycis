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

    get_children is should be a function to call containing streams in a group. Tvshows
    are a good example, they containg multiple children episodes
    """

    def __init__(self, title, url, get_children=None):
        self.title = title
        self.url = url
        self.get_children = get_children
        self.rating = None
        self.genres = []

    @property
    def code(self):
        """ return code to be used on the interface instead of its enumeration index """
        return None

    @property
    def extra_info(self):
        """ return extra info to be printed on the interface """
        return None

    @property
    def has_children(self):
        """ test if get_children function was set """
        return self.get_children != None

    def __str__(self):
        class_name = self.__class__.__name__
        fstr = u'{0}(title="{1}", url="{2}", has_children={3})'.format(
            class_name,
            self.title,
            self.url,
            self.has_children
        )

        return fstr


class Film(Media):

    def __init__(self, title, url, get_children=None, actors=None, directors=None):
        super(Film, self).__init__(name, url, get_children)

        self.actors = actors if actors else []
        self.directors = directors if directors else []


class TvShow(Media):

    def __init__(self, title, url, get_children=None, season_num=None, episode=None):
        super(TvShow, self).__init__(name, url, get_children)

        self.season_num = season_num
        self.episode_num = episode_num

    @property
    def code(self):
        if self.season_num and self.episode_num:
            return u's{0:02d}e{1:02d}'.format(self.season_num, self.episode_num)


class Song(Media):

    def __init__(self, title, url, artist=None, album=None, composer=None, get_children=None):
        super(Song, self).__init__(name, url, get_children)

        self.artist = artist
        self.album = album
        self.composer = composer
