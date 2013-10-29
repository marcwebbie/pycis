class BaseWrapper(object):

    """ BaseWrapper gives the default interface for wrappers.
    It also add utility functions to be shared by sub classes.

    Sub classes should override:
        self.site_url:
            Wrapped site base url
        get_streams(self, media):
            Get a list of stream for given Media
        search(self, search_query):
            Search wrapped site for Media objects. Return a list of Media
    """

    def __init__(self):
        self.site_url = None

    def __str__(self):
        class_name = self.__class__.__name__
        return "{}(name={}, site_url={})".format(class_name, self.name, self.site_url)

    @property
    def name(self):
        class_name = self.__class__.__name__.lower().replace('wrapper', '')
        return class_name

    def get_streams(self, media):
        raise NotImplemented("get_streams wasn't overriden by base class")

    def search(self, search_query, **search_options):
        raise NotImplemented("search wasn't overriden by base class")
