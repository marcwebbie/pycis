import logging
import re
import sys

from .base_extractor import BaseExtractor
from pycis import utils


class GorillaVidExtractor(BaseExtractor):

    """ gorillavid extractor
    """

    def __init__(self):
        # super().__init__(self)
        super(GorillaVidExtractor, self).__init__()
        self.host_list = ["gorillavid", "gorillavid.in"]
        self.holder_url = "http://gorillavid.in/embed-{}-650x400.html"
        self.regex_url = re.compile(
            r'http(s)?\://(www\.)?(?P<host>gorillavid\.in)/(embed\-)?(?P<id>\w+)(\-\w+(\.html)?)'
        )
        self.example_urls = ["http://gorillavid.in/embed-38a9c77df74ef-650x400.html"]

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
            html_embed = utils.fetch_page(dest_url)
        except:
            logging.error("Couldn't fetch page at url: {}".format(dest_url))

        url_found = re.findall(r'(http://[\w\./0-9:]+\.(?:mp4|flv))', html_embed.decode('ascii'))

        if url_found and show_progress:
            sys.stderr.write('.')
            sys.stderr.flush()

        if url_found:
            return url_found[0]
