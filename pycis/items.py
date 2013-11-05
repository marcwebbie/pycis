from collections import namedtuple

""" This module represent the base classes for wrappers sending information to interfaces

classes:
    Stream
    Media
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

    TVSHOW = "Tv Show"
    FILM = "Film"
    SONG = "Song"
    TVSHOW_EPISODE = "Tv Show Episode"

    def __init__(self, title, url, category, has_children=False):
        self.title = title
        self.url = url
        self.has_children = has_children
        self.category = category

        self.description = None
        self.rating = None
        self.genres = []
        self.year = None
        self.thumbnail = None
        self.actors = []
        self.directors = []
        self.season_num = None
        self.episode_num = None

        # song specific
        self.artist = None
        self.album = None
        self.composer = None

    @property
    def code(self):
        """ return code to be used on the interface instead of its enumeration index """
        if self.season_num and self.episode_num:
            return u's{0:02d}e{1:02d}'.format(self.season_num, self.episode_num)

    @property
    def extra_info(self):
        """ return extra info to be printed on the interface """
        return None

    def __str__(self):
        class_name = self.__class__.__name__
        fstr = u'{0}(title="{1.title!s}", url="{1.url!s}", category="{1.category!s}", has_children={1.has_children!s})'

        return fstr.format(class_name, self)
