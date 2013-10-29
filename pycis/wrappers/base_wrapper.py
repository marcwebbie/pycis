class BaseWrapper(object):

    """ BaseWrapper gives the default interface for wrappers.
    It also add utility functions to be shared by sub classes.

    Sub classes should override:
        self.name:
            Wrapper name
        self.site_url:
            Wrapped site base url
        get_streams(self, media):
            Get a list of stream for given Media
        search(self, search_query):
            Search wrapped site for Media objects. Return a list of Media
    """

    def __init__(self, name, site_url):
        self.name = name
        self.site_url = site_url

    def get_streams(self, media):
        raise NotImplemented("get_streams wasn't overriden by base class")

    def search(self, search_query, **search_options):
        raise NotImplemented("search wasn't overriden by base class")
