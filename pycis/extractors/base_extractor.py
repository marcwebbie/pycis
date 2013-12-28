import re
import sys
if sys.version_info < (3,):
    from urllib2 import urlopen, Request
    from urlparse import urljoin
else:
    from urllib.request import urlopen, Request
    from urllib.parse import urljoin


class InvalidID(Exception):
    pass


class InvalidHost(Exception):
    pass


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

    def fetch_page(self, url, extra_path=None):
        """ Download page using default user agent, read it and return its content

        If extra_path is given, it appends this path to url before request
        """

        if extra_path:
            url = urljoin(url, extra_path)

        user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0'
        headers = {'User-Agent': user_agent}
        req = Request(url, data=None, headers=headers)
        response = urlopen(req)
        content = response.read()
        return content
