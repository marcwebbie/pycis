import logging
import re
import sys
if sys.version_info < (3, 0):
    from urllib import urlencode
    from urllib2 import urlopen
else:
    from urllib.request import urlopen
    from urllib.parse import urlencode


from pyquery import PyQuery

from .base_extractor import BaseExtractor
from pycis import utils


class PutLockerExtractor(BaseExtractor):

    """ putlocker.com extractor
    """

    def __init__(self):
        # super().__init__(self)
        super(PutLockerExtractor, self).__init__()
        self.host_list = ["putlocker.com"]
        self.holder_url = "http://www.putlocker.com/embed/{}"
        self.regex_url = re.compile(
            r'(http|https)://(www\.)?(?P<host>putlocker\.(com|ws))/(embed/|file/)(?P<id>[\w]+)'
        )
        self.example_urls = ['http://www.putlocker.com/embed/AF115B1580D9C8F1',
                             'http://www.putlocker.ws/file/AF115B1580D9C8F1']

    def get_raw_url(self, video_id_or_url, show_progress=False):
        video_id = None
        if self.regex_url.match(video_id_or_url):
            video_id = self.regex_url.match(video_id_or_url).group('id')
        else:
            video_id = video_id_or_url
        dest_url = self.holder_url.format(video_id)
        logging.info("Destination url {}".format(dest_url))

        html_embed = None
        try:
            html_embed = util.fetch_page(dest_url)
        except:
            logging.info("Couldn't fetch page at url: {}".format(dest_url))

        pq = PyQuery(html_embed)

        # get form params 'fuck_you' and "confirm"
        params = {}
        params['fuck_you'] = pq('form input[name=fuck_you]').attr('value')
        params['confirm'] = pq('form input[name=confirm]').attr('value')

        # build params
        query = urlencode(params)
        if sys.version > '3':
            query = bytes(urlencode(params), encoding='utf-8')

        # request webpage again as POST with query params to get real video page
        response = urlopen(dest_url, query)
        post_html = str(response.read())

        # get api call url
        try:
            api_call = re.search(r'/get_file\.php\?stream=[\w\=]+', post_html).group()
            api_call = "http://www.putlocker.com/{}".format(api_call)
        except (IndexError, AttributeError):
            logging.info(
                ":{}:Couldn't build api call for : {}".format(self.name, video_id))
            return None

        # get api call html
        api_html = str(utils.fetch_page(api_call))

        # get video url
        url_found = None
        try:
            url_rgx = re.compile(r'url="(http://[\w\-\.\?&/\=;%]*flv|mp4|avi|m4a)"')
            url_found = url_rgx.search(api_html).group(1)
        except (IndexError, AttributeError):
            logging.info(
                ":{}:Couldn't extract url from api call: {}".format(self.name, api_call))
            return None

        if show_progress:
            if url_found:
                sys.stdout.write('.')
            else:
                sys.stdout.write('F')
            sys.stdout.flush()

        return url_found
