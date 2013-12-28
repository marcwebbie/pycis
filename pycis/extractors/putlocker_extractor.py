import logging
import re
import sys

import requests
from pyquery import PyQuery

from .base_extractor import BaseExtractor


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
            html_embed = request.get(dest_url).text
        except:
            logging.info("Couldn't fetch page at url: {}".format(dest_url))

        pq = PyQuery(html_embed)

        # get form params 'fuck_you' and "confirm"
        params = {}
        params['fuck_you'] = pq('form input[name=fuck_you]').attr('value')
        params['confirm'] = pq('form input[name=confirm]').attr('value')

        headers = {
            "Referer": dest_url,
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1674.0 Safari/537.36"
        }

        # request webpage again as POST with query params to get real video page
        api_response = requests.post(dest_url, params, headers=headers)

        # get api call url
        try:
            api_call = re.search(r'/get_file\.php\?stream=[\w\=]+', api_response.text).group()
            api_call = "http://www.putlocker.com/{}".format(api_call)
        except (IndexError, AttributeError):
            logging.error(":{}:Couldn't build api call for : {}".format(self.name, video_id))
            return None

        # get api call html
        api_html = requests.get(api_call).text

        # get video url
        url_found = None
        try:
            url_rgx = re.compile(r'url="(http://[\w\-\.\?&/\=;%]*flv|mp4|avi|m4a)"')
            url_found = url_rgx.search(api_html).group(1)
        except (IndexError, AttributeError):
            logging.error(":{}:Couldn't extract url from api call: {}".format(self.name, api_call))
            return None

        if show_progress:
            if url_found:
                sys.stdout.write('.')
            else:
                sys.stdout.write('F')
            sys.stdout.flush()

        return url_found
