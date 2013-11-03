import re
import sys
if sys.version_info < (3,):
    from urllib2 import urlopen, Request
else:
    from urllib.request import urlopen, Request


class BaseExtractor(object):

    def __init__(self):
        self.regex_url = None
        self.host_list = None
        self.holder_url = None
        self.regex_url = None
        self.example_urls = None

    def is_valid_host(self, host):
        return host in self.host_list

    def is_valid_url(self, url):
        return re.match(self.regex_url, url)

    def get_id(self, url):
        if self.is_valid_url(url):
            try:
                re.match(self.regex_url, url).group('id')
            except:
                raise InvalidID('Not a valid id')

    def get_host(self, url):
        if self.is_valid_url(url):
            try:
                re.match(self.regex_url, url).group('host')
            except:
                raise InvalidHost('Not a valid host')

    @property
    def name(self):
        return self.__class__.__name__.lower()

    def __str__(self):
        s = "{0}(name={1}, host_list={2})".format(
            self.__class__.__name__,
            self.name,
            self.host_list
        )

        return s
